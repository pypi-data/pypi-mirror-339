import asyncio
import glob
import os
import time
from asyncio import CancelledError
from datetime import datetime
from enum import Enum
from functools import wraps
from typing import Callable, Dict, List, Optional, Tuple, Union

import asyncclick as click
import httpx
from cron_descriptor import get_description as get_schedule_description
from croniter import croniter
from InquirerPy import get_style, inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.status import Status

from omegacloud_cli import api
from omegacloud_cli.common.enums import (
    AgentStatusEnum,
    JobStatusEnum,
    JobTypeEnum,
    TaskStatusEnum,
)
from omegacloud_cli.common.schemas import (
    AgentStatusResponseModel,
    TaskStatusResponseModel,
)
from omegacloud_cli.controllers.filesync import FileSyncManager
from omegacloud_cli.utils import load_config, load_script, save_config, save_script

# Command aliases
ALIASES = {
    "start": "run",
    "logs": "watch",
    "log": "watch",
    "status": "inspect",
    "files": "sync",
}

style = get_style({"question": "bold"}, style_override=False)

console = Console()


def try_except_wrapper(func):
    """
    A decorator that wraps functions with common error handling logic.
    Handles KeyboardInterrupt, CancelledError, HTTPStatusError, ConnectError and general exceptions.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (KeyboardInterrupt, CancelledError):
            console.print("[yellow]Operation cancelled.[/]")
            console.print()
            return None
        except httpx.HTTPStatusError as e:
            if e.response.status_code in [401, 403]:
                console.print("[red]Authentication failed. Please login by > omega login.[/]")
            elif e.response.status_code in [500]:
                console.print(f"[red]An error occurred: {str(e)}[/]")
            else:
                console.print(f"[red]An error occurred: {str(e)}[/]")
            raise click.Abort()
        except httpx.ConnectError as e:
            console.print(
                f"[red]Omega Platform is now unavailable. Please try again later. {str(e)}[/]"
            )
            raise click.Abort()
        except Exception as e:
            console.print(f"[red]An error occurred: {str(e)}[/]")
            raise click.Abort()

    return wrapper


def check_auth_wrapper(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        """Check if user is authenticated and initiate login flow if not."""
        if not load_config("apikey"):
            console.print("[yellow]Authentication required[/]")
            await login_flow()
        return await func(*args, **kwargs)

    return wrapper


# Custom Click Group to handle aliases
class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        # Resolve alias to the actual command
        cmd_name = ALIASES.get(cmd_name, cmd_name)
        return super().get_command(ctx, cmd_name)


@click.group(cls=AliasedGroup)
def cli():
    """
    OmegaCloud: One-click platform for AI-apps deployment
    """
    pass


@cli.command(name="login", help="Login to Omega Cloud")
async def cli_login():
    """Login to Omega Cloud."""
    await login_flow()


@cli.command(name="run", help="Run a new Job | aliases: start")
@check_auth_wrapper
@try_except_wrapper
async def cli_run():
    """Start a new job"""
    with console.status("") as status:
        await run_flow(status)


@cli.command(name="stop", help="Stop a running job")
@check_auth_wrapper
@try_except_wrapper
async def cli_stop():
    """Stop a running job."""
    with console.status("") as status:
        await stop_flow(status)


@cli.command(name="inspect", help="Get status of a job | aliases: status")
@check_auth_wrapper
@try_except_wrapper
async def cli_inspect():
    """Get status of a job."""
    with console.status("") as status:
        await inspect_flow(status)


@cli.command(name="watch", help="Watch logs from the job | aliases: logs")
@check_auth_wrapper
@try_except_wrapper
async def cli_watch():
    """Watch logs from the job."""
    with console.status("") as status:
        await watch_flow(status)


@cli.command(name="sync", help="Synchronize files | aliases: files")
@check_auth_wrapper
@try_except_wrapper
async def cli_sync():
    """Synchronize files with the job."""
    with console.status("[bold cyan]Analyzing files for sync...[/]") as status:
        if load_config("job_schedule"):
            sync_type = "task"
        else:
            sync_type = "agent"
        await sync_flow(status, sync_type=sync_type, operations="upload+download")


@cli.command(name="config", help="Configure Omega Run")
@check_auth_wrapper
@try_except_wrapper
async def cli_config():
    """Configure CLI parameters."""

    """Check if there are any running processes that would prevent configuration changes."""
    agent_id = get_agent_id(raise_error=False)
    agent_info = await inspect_agent(agent_id)
    if agent_info and agent_info.agent_status in [AgentStatusEnum.BUSY, AgentStatusEnum.IDLE]:
        console.print("[red]Cannot modify configuration while application is running[/]")
        raise click.Abort()

    task_id = get_task_id(raise_error=False)
    task_info = await inspect_task(task_id)
    if task_info and task_info.task_status == TaskStatusEnum.ON:
        console.print("[red]Cannot modify configuration while job is scheduled[/]")
        raise click.Abort()

    with console.status("") as status:
        await config_flow(status, force_config=True)


# FLOWS


async def login_flow():
    """Handle user login flow."""
    console.print()
    console.print("Please visit: [bold]https://omegacloud.ai/user[/]")
    console.print("Get your access token and paste it below")
    console.print()

    token = await inquirer.text(
        message="Enter your access token:",
        style=style,
    ).execute_async()

    save_config({"apikey": token})
    console.print("[green]Token saved successfully[/]")
    console.print("You can update your token anytime by running: [bold]omega login[/]")
    console.print()


async def sync_flow(status: Status, sync_type: str, operations: str = "upload+download") -> bool:
    """
    File Synchronization Procedure
    """

    status.update("[bold cyan]Syncing files...[/]")
    sync_error = False

    if sync_type == "task":
        sync_id = get_task_id()
    else:
        sync_id = get_agent_id()

    sync_dirs = []
    sync_dirs.append({"path": os.getcwd(), "storage_name": ""})
    storage_list = load_config("storage")
    for storage_name in storage_list:
        sync_dirs.append(
            {
                "path": os.path.join(os.getcwd(), ".omega", "storage", storage_name),
                "storage_name": storage_name,
            }
        )

    for sync_dir in sync_dirs:
        storage_path = sync_dir["path"]
        storage_name = sync_dir["storage_name"]

        if storage_name:
            status.update(f"[bold cyan]Syncing storage '{storage_name}'...[/]")

        # Create snapshot for this directory
        snapshot = await FileSyncManager.create_snapshot(storage_path)

        # Get sync actions from the server
        sync_result = await api.sync_files_api(
            sync_type,
            sync_id,
            snapshot,
            storage_name,
        )

        to_client_count = len(sync_result.to_client)
        to_server_count = len(sync_result.to_server)

        # Stop the status completely before starting the progress display
        # to avoid overlap between status and progress
        status.stop()

        if (to_client_count == 0 or "download" not in operations) and (
            to_server_count == 0 or "upload" not in operations
        ):
            if storage_name:
                console.print(f"[green]All files are in sync @ {storage_name}[/]")
            else:
                console.print("[green]All files are in sync[/]")
            console.print()
            status.start()
            continue

        elif (to_client_count == 0 or "download" not in operations) and to_server_count > 0:
            # no need to ask, just upload
            choice = "upload"

        else:
            # Print sync summary
            if storage_name:
                console.print(f"\n[cyan]File-sync status @ {storage_name}[/]")
            else:
                console.print("\n[cyan]File-sync status:[/]")

            if to_client_count > 0:
                console.print(f"Files to download: [bold]{to_client_count}[/]")
                for file in sync_result.to_client[:10]:
                    console.print(f" - {file.path}")
                if to_client_count > 10:
                    console.print(f" - and {to_client_count - 10} more...")
                console.print()

            if to_server_count > 0:
                console.print(f"Files to upload: [bold]{to_server_count}[/]")
                for file in sync_result.to_server[:10]:
                    console.print(f" - {file.path}")
                if to_server_count > 10:
                    console.print(f" - and {to_server_count - 10} more...")
                console.print()

            # Ask for confirmation before proceeding
            if to_client_count * to_server_count > 0:
                choices = [
                    Choice(value="all", name="Proceed with sync"),
                    Choice(value="download", name="Download only"),
                    Choice(value="upload", name="Upload only"),
                    Choice(value="cancel", name="Cancel"),
                ]
            else:
                choices = [
                    Choice(value="all", name="Proceed with sync"),
                    Choice(value="cancel", name="Cancel"),
                ]

            # Use the async version of select
            choice = await inquirer.select(
                message="Do you want to proceed with the sync?",
                choices=choices,
                default=choices[0].value,
                style=style,
            ).execute_async()

        if choice == "cancel":
            console.print("[yellow]Operation cancelled.[/]")
            status.start()
            sync_error = True
            continue

        # Add a blank line to create separation
        console.print()

        # Execute sync operations with Progress
        with Progress() as progress:
            # Process downloads first if stopping
            if to_client_count > 0 and choice in ["all", "download"]:
                console.print("Downloading files from server...")

                # Create individual tasks for each download
                download_tasks = {}
                for file_meta in sync_result.to_client:
                    # Create a task with the file size as the total
                    download_task_id = progress.add_task(
                        f"[green]Downloading {file_meta.path}[/]", total=file_meta.size, completed=0
                    )
                    download_tasks[file_meta.path] = download_task_id

                # Process each download
                for file_meta in sync_result.to_client:
                    download_task_id = download_tasks[file_meta.path]
                    download_callback = make_progress_callback(progress, download_task_id)

                    success, error = await api.download_file_api(
                        sync_type,
                        sync_id,
                        file_meta.path,
                        storage_path,
                        storage_name,
                        download_callback,
                    )

                    if success:
                        progress.update(
                            download_task_id,
                            completed=file_meta.size,
                            description=f"[green]Completed: {file_meta.path}[/]",
                        )
                    elif error:
                        sync_error = True
                        console.print(f"[red]Failed download {file_meta.path}: {str(error)}[/]")
                        progress.update(
                            download_task_id,
                            completed=file_meta.size,
                            description=f"[red]Failed: {file_meta.path}",
                        )
                    else:
                        sync_error = True
                        console.print(f"[red]Failed download {file_meta.path}[/]")
                        progress.update(
                            download_task_id,
                            completed=file_meta.size,
                            description=f"[red]Failed: {file_meta.path}",
                        )

            # Process uploads first if starting
            if to_server_count > 0 and choice in ["all", "upload"]:
                console.print("[blue]Uploading files to server...[/]")

                # Create individual tasks for each upload
                upload_tasks = {}
                for file_meta in sync_result.to_server:
                    # Create a task with the file size as the total
                    upload_task_id = progress.add_task(
                        f"[blue]Uploading {file_meta.path}", total=file_meta.size, completed=0
                    )
                    upload_tasks[file_meta.path] = upload_task_id

                # Process each upload
                for file_meta in sync_result.to_server:
                    upload_task_id = upload_tasks[file_meta.path]
                    upload_callback = make_progress_callback(progress, upload_task_id)

                    success, error = await api.upload_file_api(
                        sync_type,
                        sync_id,
                        file_meta.path,
                        storage_path,
                        storage_name,
                        upload_callback,
                    )

                    if success:
                        progress.update(
                            upload_task_id,
                            completed=file_meta.size,
                            description=f"[blue]Completed: {file_meta.path}",
                        )
                    elif error:
                        sync_error = True
                        console.print(f"[red]Failed upload {file_meta.path}: {str(error)}[/]")
                        progress.update(
                            upload_task_id,
                            completed=file_meta.size,
                            description=f"[red]Failed: {file_meta.path}",
                        )
                    else:
                        sync_error = True
                        console.print(f"[red]Failed upload {file_meta.path}[/]")
                        progress.update(
                            upload_task_id,
                            completed=file_meta.size,
                            description=f"[red]Failed: {file_meta.path}",
                        )

    synced = not sync_error

    console.print("[green]Sync completed![/]")
    console.print()
    status.start()
    return synced


async def watch_flow(status: Status):
    status.update("[bold cyan]Watching for the logs... (safe to CTRL+C)[/]")
    console.print()
    if agent_id := get_agent_id(raise_error=False):
        watch_type = "agent"
        watch_id = agent_id
    elif task_id := get_task_id(raise_error=False):
        watch_type = "task"
        watch_id = task_id

    if watch_id:
        async for line in api.watch_api(watch_type, watch_id):
            console.print(line.strip(), highlight=False, markup=False)
    else:
        console.print("[red]Nothing to watch[/]")


async def inspect_flow(status: Status):
    status.update("[bold cyan]Inspecting your application...[/]")

    # job_type = load_config("job_type")
    job_schedule = load_config("job_schedule")

    if agent_id := get_agent_id(raise_error=False):
        agent_info = await inspect_agent(agent_id)
        info_dict = agent_info.model_dump()

        job_status = agent_info.job_status or JobStatusEnum.STOPPED
        job_status_value = job_status.value.upper()

        if (
            not agent_info
            or not agent_info.agent_status
            or agent_info.agent_status in [AgentStatusEnum.DEAD]
        ):
            console.print("[red]No active environment found[/]")
        elif agent_info.agent_status in [AgentStatusEnum.INIT]:
            console.print("[yellow]Application is initializing[/]")
        elif agent_info.agent_status in [AgentStatusEnum.IDLE]:
            console.print("[yellow]Application is not running[/]")
        elif agent_info.agent_status in [AgentStatusEnum.BUSY]:
            console.print("[green]Application is running[/]")
        else:
            console.print(f"[red]Unknown status: {job_status_value}[/]")
            raise click.Abort()

        for key, val in info_dict.items():
            title = key.replace("_", " ").title()
            title = title.replace("Agent", "Environment")
            value = val.value.upper() if isinstance(val, Enum) else val
            if "logs" not in key:
                if value:
                    console.print(f"{title}: {value}")
            else:
                print_logs("Application Logs", val)

        console.print()

    if (task_id := get_task_id(raise_error=False)) and job_schedule:
        task_info = await inspect_task(task_id)
        info_dict = task_info.model_dump()

        task_status = task_info.task_status
        if not task_info or not task_info.task_status:
            console.print("[red]No scheduled job found[/]")
        elif task_status == TaskStatusEnum.ON:
            console.print("[green]Scheduled job is enabled[/]")
        elif task_status == TaskStatusEnum.OFF:
            console.print("[yellow]Scheduled job is disabled[/]")
        else:
            console.print(f"[red]Unknown status: {task_status}[/]")
            raise click.Abort()

        for key, val in info_dict.items():
            title = key.replace("_", " ").title()
            value = val.value.upper() if isinstance(val, Enum) else val
            if "schedule" in key:
                console.print(f"{title} (cron): {value}")
                console.print(f"{title}: {get_schedule_description(value)}")
            elif "logs" not in key:
                if value:
                    console.print(f"{title}: {value}")
            elif not agent_id:
                print_logs("Scheduled Job Logs", val)

        console.print()


async def disk_flow():
    # Ask user to input disk size

    # Read previous disk size from config file
    compute_size = load_config("compute_size", None)
    compute_size_type = compute_size.split("-")[0] if compute_size else None

    if compute_size_type == "cpu":
        disk_min = 8
        disk_max = 1000
        disk_size_default = "12"
    else:
        disk_min = 30
        disk_max = 1000
        disk_size_default = "50"

    disk_size = load_config("disk_size", disk_size_default)

    while True:
        disk_size = await inquirer.text(
            message=f"Enter disk size in GB [{disk_min}-{disk_max}]:",
            default=disk_size,
            style=style,
        ).execute_async()

        try:
            disk_size_int = int(disk_size)
            if disk_min <= disk_size_int <= disk_max:
                break
            else:
                console.print(f"[red]Disk size must be between {disk_min} and {disk_max} GB.[/]")
        except ValueError:
            console.print("[red]Please enter a valid number.[/]")

    # Save the selected disk size to config file
    save_config({"disk_size": disk_size})

    return disk_size


async def schedule_flow() -> str:
    schedule_mapping = {
        "once": "",
        "hourly": "0 * * * *",
        "daily": "0 0 * * *",
        "weekly": "0 0 * * 0",
        "monthly": "0 0 1 * *",
    }

    schedule_mapping_reverse = {v: k for k, v in schedule_mapping.items()}
    job_schedule = load_config("job_schedule", "0 0 * * *")
    schedule_choice = schedule_mapping_reverse.get(job_schedule, "custom")

    choices = [
        Choice(value="once", name="Once"),
        Choice(value="hourly", name="Every hour"),
        Choice(value="daily", name="Every day"),
        Choice(value="weekly", name="Every week"),
        Choice(value="monthly", name="Every month"),
        Choice(value="custom", name="Custom"),
    ]

    schedule_choice = await inquirer.select(
        message="Select job schedule:",
        choices=choices,
        default=schedule_choice,
        style=style,
    ).execute_async()

    job_schedule_input = schedule_mapping.get(schedule_choice, None)
    if job_schedule_input is not None:
        job_schedule = job_schedule_input
    else:
        console.print("Input cron schedule for your job")
        console.print("For reference, visit: [bold]https://crontab.guru/[/bold]")

        # Loop until valid cron format is entered
        valid_format = False
        while not valid_format:
            job_schedule = await inquirer.text(
                message="Cron schedule:",
                style=style,
                default=job_schedule,
            ).execute_async()
            valid_format = validate_cron_format(job_schedule)
            if not valid_format:
                console.print("[red]Invalid cron format. Please try again.[/red]")
            else:
                console.print(f"Your schedule: {get_schedule_description(job_schedule)}")
                # ask confirmation
                choices = [
                    Choice(value="yes", name="Yes"),
                    Choice(value="no", name="No"),
                ]
                confirmation = await inquirer.select(
                    message="Is this correct?",
                    choices=choices,
                ).execute_async()
                if confirmation == "no":
                    valid_format = False

    save_config({"job_schedule": job_schedule})

    # Load task.sh script for user display
    script = load_script("task.sh")
    task_command = " && ".join(script) if script else "python main.py"

    # Ask user to input task run command
    task_command = await inquirer.text(
        message="Enter command to run your task:",
        style=style,
        default=task_command,
    ).execute_async()

    # Split command by && and clean up whitespace
    commands = [cmd.strip() for cmd in task_command.split("&&")]
    save_script("task.sh", commands)

    return job_schedule


async def type_flow() -> Tuple[JobTypeEnum, str]:
    detected_job_type = await detect_job_type()
    job_type = load_config("job_type", detected_job_type.value)

    choices = [
        Choice(value="api", name="API - Start an API-service (FastAPI/Flask)"),
        Choice(value="job", name="Job - Run a program (one-time or periodically)"),
        Choice(value="lab", name="Lab - Launch a Lab (Jupyter Notebook)"),
    ]

    job_type = await inquirer.select(
        message="Select your run type:",
        choices=choices,
        default=job_type,
        style=style,
    ).execute_async()

    if job_type == "job":
        job_schedule = await schedule_flow()

    elif job_type == "api":
        # Ask if user wants to add a schedule job for the API
        choices = [
            Choice(value="no", name="No, just run API"),
            Choice(value="yes", name="Yes, add scheduled job"),
        ]
        schedule_task = await inquirer.select(
            message="Would you like to add a scheduled job on top of your API?",
            choices=choices,
            default=choices[0].value,
            style=style,
        ).execute_async()

        if schedule_task == "yes":
            job_schedule = await schedule_flow()
        else:
            job_schedule = ""

    elif job_type == "lab":
        job_schedule = ""

    save_config({"job_type": job_type, "job_schedule": job_schedule})

    return JobTypeEnum(job_type), job_schedule


async def storage_procedure():
    """Ask user to type storage names, separated by commas. return list of storage names."""

    # Read previous disk size from config file
    storage_list = load_config("storage", [])

    console.print("Shared storage is sync automatically between your jobs")
    storage_text = await inquirer.text(
        message="Enter shared storage names:",
        style=style,
        default=", ".join(storage_list),
    ).execute_async()

    storage_list = storage_text.split(",")
    storage_list = [s.strip() for s in storage_list if s.strip()]
    save_config({"storage": storage_list})

    return storage_list


async def size_flow(job_type: JobTypeEnum, force_config: bool = False):
    title = get_job_title(job_type)
    compute_size = load_config("compute_size", None)

    # Get compute options from API
    compute_options = await api.get_compute_options_api()

    # Separate CPU and GPU options
    cpu_options = [opt for opt in compute_options if opt.code.startswith("cpu")]
    gpu_options = [opt for opt in compute_options if opt.code.startswith("gpu")]

    cpu_price_min = min([o.price for o in cpu_options]) * 750  # month
    cpu_price_max = max([o.price for o in cpu_options]) * 750  # month
    gpu_price_min = min([o.price for o in gpu_options])  # hour
    gpu_price_max = max([o.price for o in gpu_options])  # hour

    if (compute_size is None or force_config) and job_type != JobTypeEnum.LAB:
        # Create top level choices for CPU vs GPU
        cpu_choice = Choice(
            value="cpu",
            name=f"CPU (${cpu_price_min:.2f} .. ${cpu_price_max:.2f}/month)",
        )
        gpu_choice = Choice(
            value="gpu",
            name=f"GPU (${gpu_price_min:.2f} .. ${gpu_price_max:.2f}/hour)",
        )

        choices = [cpu_choice, gpu_choice]

        compute_size = await inquirer.select(
            message=f"Select compute for your {title}:",
            choices=choices,
            default=choices[0].value,
            style=style,
        ).execute_async()
        compute_size = f"{compute_size}-m"

    if job_type == JobTypeEnum.LAB or ("gpu" in compute_size):
        # Calculate max lengths for formatting
        max_title_length = max([len(opt.title) for opt in gpu_options]) + 2
        max_desc_length = max([len(opt.description) for opt in gpu_options]) + 2

        # Create choices for GPU sizes
        choices = [
            Choice(
                value=opt.code,
                name=f"{opt.title:{max_title_length}} : {opt.description:{max_desc_length}} : {opt.price_tag}",
            )
            for opt in gpu_options
        ]

        compute_size = await inquirer.select(
            message=f"Select GPU size for your {title}:",
            choices=choices,
            default=compute_size,
            style=style,
        ).execute_async()

    else:
        # Calculate max lengths for formatting
        max_title_length = max([len(opt.title) for opt in cpu_options]) + 2
        max_desc_length = max([len(opt.description) for opt in cpu_options]) + 2

        # Create choices for CPU sizes
        choices = [
            Choice(
                value=opt.code,
                name=f"{opt.title:{max_title_length}} : {opt.description:{max_desc_length}} : {opt.price_tag}",
            )
            for opt in cpu_options
        ]

        compute_size = await inquirer.select(
            message=f"Select compute for your {title}:",
            choices=choices,
            default=compute_size,
            style=style,
        ).execute_async()

    save_config({"compute_size": compute_size})

    return compute_size


async def env_flow() -> Tuple[str, Optional[str], Optional[Dict[str, str]]]:
    """
    Ask user to select environment variables configuration.
    Returns:
        Tuple containing:
        - env_type: "file" or "values"
        - env_file: filename if env_type == "file", None otherwise
        - env_values: dict of values if env_type == "values", None otherwise
    """
    env_type = load_config("env_type")
    env_file = load_config("env_file")

    # Find all .env* files in the current directory
    env_files = glob.glob(".env*")

    # Determine which options to present based on found env files
    if env_files:
        # Multiple .env files found - let user choose one or enter custom values
        choices = [Choice(value=f, name=f"Use {f} file") for f in env_files]
        choices.append(Choice(value="custom", name="Enter manually"))

        selected = await inquirer.select(
            message="Select environment variables:",
            choices=choices,
            default=env_file if env_file in [c.value for c in choices] else choices[-1].value,
            style=style,
        ).execute_async()

    else:
        # No .env files found - collect environment variables manually
        console.print(
            "[yellow]No .env files found in current directory. Provide ENV one-by-one.[/]"
        )
        console.print("Format: KEY=VALUE. To finish, press ENTER")
        selected = "custom"

    if selected == "custom":
        env_type = "values"
        env_file = None
        env_values = await collect_env_values()
    else:
        env_type = "file"
        env_file = selected
        env_values = None

    # Save the configuration
    save_config({"env_type": env_type, "env_file": env_file, "env_values": env_values})

    return env_type, env_file, env_values


async def config_flow(status: Status, force_config: bool = False) -> dict:
    """
    Configuration Flow
    Handles all configuration settings with strict validation.
    """
    config = {}

    # Stop the status to avoid interference with questions
    status.stop()

    # Job type configuration
    job_type_value = load_config("job_type")
    if force_config or job_type_value is None:
        job_type, job_schedule = await type_flow()
        config["job_type"] = job_type.value
        config["job_schedule"] = job_schedule
    else:
        job_schedule = load_config("job_schedule")
        config["job_type"] = job_type_value
        config["job_schedule"] = job_schedule
        job_type = JobTypeEnum(job_type_value)

    # Compute size configuration (CPU/GPU)
    compute_size_value = load_config("compute_size")
    if force_config or compute_size_value is None:
        config["compute_size"] = await size_flow(job_type, force_config)
    else:
        config["compute_size"] = compute_size_value

    # Disk size configuration
    disk_size_value = load_config("disk_size")
    if force_config or disk_size_value is None:
        disk_size = await disk_flow()
        config["disk_size"] = disk_size
    else:
        config["disk_size"] = disk_size_value

    # Storage configuration
    storage_value = load_config("storage")
    if force_config or storage_value is None:
        storage = await storage_procedure()
        config["storage"] = storage
    else:
        config["storage"] = storage_value

    # Environment variables configuration
    env_type_value = load_config("env_type")
    if force_config or env_type_value is None:
        env_type, env_file, env_values = await env_flow()
        config["env_type"] = env_type
        config["env_file"] = env_file
        config["env_values"] = env_values
    else:
        config["env_type"] = load_config("env_type")
        config["env_file"] = load_config("env_file")
        config["env_values"] = load_config("env_values", {})

    # Validate the complete configuration
    try:
        validate_config(config)
    except ValueError as e:
        console.print(f"[red]Configuration error: {str(e)}[/]")
        raise click.Abort()

    # Save the full configuration
    save_config(config)

    # Start the status again
    status.start()

    return config


async def run_task_flow(status: Status, fixed_agent_id: Optional[str] = None) -> str:
    """
    Steps:
    1. Inspect task status
    2. Create task if not exists
    3. If task is OFF, sync files and enable task
    4. If task is ON, check job status and offer to run immediately
    """
    status.update("[bold cyan]Checking the scheduled job...[/]")

    task_id = get_task_id(raise_error=False)
    task_info = await inspect_task(task_id)

    if not task_id or not task_info.task_status:
        console.print("- Scheduled job not found. Creating...")
        status.update("[bold cyan]Creating the scheduled job...[/]")

        task_info = await api.init_task_api(
            size=load_config("compute_size"),
            disk_size=load_config("disk_size"),
            storage=load_config("storage"),
            environment=get_environment_variables(),
            schedule=load_config("job_schedule"),
            setup_cmd=load_script("setup.sh"),
            run_cmd=load_script("task.sh"),
            build_cmd=load_script("build.sh"),
            fixed_agent_id=fixed_agent_id,
        )
        task_id = task_info.task_id
        save_config({"task_id": task_id})
        task_info = await inspect_task(task_id)

    if task_info.task_status == TaskStatusEnum.OFF:
        console.print("- Scheduled job initialized. Enabling...")

        # sync
        job_type = JobTypeEnum(load_config("job_type"))
        if job_type == JobTypeEnum.JOB:
            files_are_synced = await sync_flow(status, sync_type="task", operations="upload")
            if not files_are_synced:
                raise KeyboardInterrupt

        status.update("[bold cyan]Enabling the scheduled job...[/]")
        task_info = await api.enable_task_api(
            task_id,
            schedule=load_config("job_schedule"),
            setup_cmd=load_script("setup.sh"),
            run_cmd=load_script("task.sh"),
            build_cmd=load_script("build.sh"),
            fixed_agent_id=fixed_agent_id,
        )

    if task_info.task_status == TaskStatusEnum.ON:
        console.print("- Scheduled job enabled")
        if task_info.job_status != JobStatusEnum.RUNNING:
            # ask user to start now
            task_action = await ask(
                status,
                "Do you want to run your job now?",
                [
                    ("yes", "Yes, run it now"),
                    ("no", "No, wait for schedule"),
                ],
            )
            if task_action == "no":
                return

            task_info = await api.run_task_api(task_id)
            console.print("- Scheduled job initialized")
            max_wait_time = 60  # sec
            sleep_time = 3  # sec
            start_time = time.time()
            while (time.time() - start_time) < max_wait_time:
                status.update("[bold cyan]Starting the job...[/]")
                await asyncio.sleep(sleep_time)
                task_info = await inspect_task(task_id)
                if task_info.job_status == JobStatusEnum.RUNNING:
                    break

    if task_info.task_status == TaskStatusEnum.ON and task_info.job_status == JobStatusEnum.RUNNING:
        await watch_flow(status)


async def run_agent_flow(status: Status):
    """
    Steps:
    1. Inspect agent status
    2. Create agent if not exists
    3. Wait for IDLE status (break if DEAD)
    3. Sync files
    4. Run process
    """
    status.update("[bold cyan]Checking the runtime environment...[/]")

    # get agent status
    agent_id = get_agent_id(raise_error=False)
    agent_info = await inspect_agent(agent_id)

    if (
        not agent_id
        or not agent_info.agent_status
        or agent_info.agent_status == AgentStatusEnum.DEAD
    ):
        console.print("- Environment not found. Creating...")
        status.update("[bold cyan]Creating the environment...[/]")

        agent_info = await api.init_agent_api(
            load_config("compute_size"),
            load_config("disk_size"),
            load_config("storage"),
            get_environment_variables(),
            JobTypeEnum(load_config("job_type")),
            load_script("setup.sh"),
            load_script("run.sh"),
            load_script("build.sh"),
        )
        agent_id = agent_info.agent_id
        save_config({"agent_id": agent_id})
        console.print("- Environment initialized. Starting...")

        while agent_info.agent_status != AgentStatusEnum.INIT:
            await asyncio.sleep(1)
            agent_info = await inspect_agent(agent_id)

    status_text = None
    while agent_info.agent_status == AgentStatusEnum.INIT:
        status.update("[bold cyan]Starting the environment...[/]")

        await asyncio.sleep(1)
        agent_info = await inspect_agent(agent_id)

        if (
            agent_info.agent_status_text
            and agent_info.agent_status_text != status_text
            and agent_info.agent_status in [AgentStatusEnum.INIT]
        ):
            status_text = agent_info.agent_status_text
            console.print(f"- {status_text}")

        # Break if status becomes DEAD during initialization
        if agent_info.agent_status == AgentStatusEnum.DEAD:
            console.print("[red]Environment failed[/]")
            print_logs("Agent Logs", agent_info.agent_logs)
            raise click.Abort()

    if agent_info.agent_status == AgentStatusEnum.IDLE:
        files_are_synced = await sync_flow(status, sync_type="agent", operations="upload")
        if not files_are_synced:
            raise KeyboardInterrupt

        agent_info = await api.run_agent_api(agent_id)
        console.print("- Environment ready. Starting application...")

    while agent_info.agent_status != AgentStatusEnum.BUSY:
        status.update("[bold cyan]Starting the application...[/]")
        await asyncio.sleep(1)
        agent_info = await inspect_agent(agent_id)
        # Break if status becomes DEAD during initialization
        if agent_info.agent_status == AgentStatusEnum.DEAD:
            console.print("[red]Application failed[/]")
            print_logs("Agent Logs", agent_info.agent_logs)
            raise click.Abort()

    if agent_info.agent_status == AgentStatusEnum.BUSY:
        console.print("- Application is running")
        agent_info = await inspect_agent(agent_id)
        if agent_info.job_url:
            console.print(f"Application URL: {agent_info.job_url}")
            console.print()
        job_type = JobTypeEnum(load_config("job_type"))
        if not load_config("job_schedule") and job_type != JobTypeEnum.LAB:
            await watch_flow(status)


async def run_flow(status: Status) -> None:
    """
    Run Flow - Initiates and starts an application based on its type.
    Decision Tree:
    - Lab Application: RUN_AGENT_PROCEDURE
    - API Only Application: RUN_AGENT_PROCEDURE
    - API + Scheduled Job: RUN_AGENT_PROCEDURE + RUN_TASK_PROCEDURE
    - One-time Job: RUN_AGENT_PROCEDURE
    - Scheduled Job: RUN_TASK_PROCEDURE
    """
    await config_flow(status)

    job_type = JobTypeEnum(load_config("job_type"))
    job_schedule = load_config("job_schedule")

    # Scheduled Job - only needs task procedure
    if job_type == JobTypeEnum.LAB:
        await run_agent_flow(status)

    if job_type == JobTypeEnum.API and not job_schedule:
        # API Only Application
        await run_agent_flow(status)

    if job_type == JobTypeEnum.API and job_schedule:
        # API + Scheduled Job
        await run_agent_flow(status)
        await run_task_flow(status, get_agent_id())

    if job_type == JobTypeEnum.JOB and not job_schedule:
        # One-time Job
        await run_agent_flow(status)

    if job_type == JobTypeEnum.JOB and job_schedule:
        # Scheduled Job
        await run_task_flow(status)


async def stop_agent_flow(status: Status, agent_id: str) -> bool:
    """
    Steps:
    1. Inspect agent status
    2. Stop running process
    3. Sync files in IDLE state
    4. Terminate agent (LAB type always terminates)
    """
    agent_info = await inspect_agent(agent_id)

    # If agent is not running, nothing to do
    if (
        not agent_info
        or not agent_info.agent_status
        or agent_info.agent_status
        not in [
            AgentStatusEnum.INIT,
            AgentStatusEnum.BUSY,
            AgentStatusEnum.IDLE,
        ]
    ):
        console.print("[green]No application to stop[/]")
        console.print()
        return True

    # Stop initizlizing agent
    if agent_info.agent_status == AgentStatusEnum.INIT:
        status.update("[bold cyan]Stopping initialization...[/]")
        await api.kill_agent_api(agent_id)
        console.print("[green]Initialization stopped[/]")
        console.print()
        return True

    # Stop running process if busy
    if agent_info.agent_status == AgentStatusEnum.BUSY:
        status.update("[bold cyan]Stopping your application...[/]")
        await api.stop_agent_api(agent_id)

        # Wait for IDLE state
        while agent_info.agent_status != AgentStatusEnum.IDLE:
            await asyncio.sleep(1)
            agent_info = await inspect_agent(agent_id)

    # Sync files in IDLE state if required
    if agent_info.agent_status == AgentStatusEnum.IDLE:
        console.print("[green]Application stopped[/]")
        console.print()
        await sync_flow(status, sync_type="agent", operations="download")

    if agent_info.job_type == JobTypeEnum.LAB:
        terminate_answer = "terminate"
    else:
        # ask user to terminate agent
        terminate_answer = await ask(
            status,
            "Do you want to terminate runtime environment?",
            [
                ("terminate", "Yes, terminate"),
                ("keep", "No, keep it running"),
            ],
        )
    if terminate_answer == "terminate":
        status.update("[bold cyan]Terminating environment...[/]")
        agent_info = await api.kill_agent_api(agent_id)

    if agent_info.agent_status == AgentStatusEnum.DEAD:
        print_costs(agent_info)
        console.print("[green]Application stopped. Environment terminated[/]")
        console.print()
    elif agent_info.agent_status == AgentStatusEnum.IDLE:
        console.print("[green]Application stopped. Environment still running.[/]")
        console.print()

    return True


async def stop_task_flow(status: Status, task_id: str) -> bool:
    """
    Steps:
    1. Inspect task status
    2. Handle running job
    3. Disable task
    """

    status.update("[bold cyan]Checking the scheduled job...[/]")
    task_info = await inspect_task(task_id)

    # If task is not enabled, nothing to do
    if not task_info or not task_info.task_status:
        console.print("[red]Scheduled job not found[/]")
        console.print()
        return True

    if task_info.task_status == TaskStatusEnum.ON:
        if task_info.job_status == JobStatusEnum.RUNNING:
            console.print("- Scheduled job is running. Stopping...")
            status.update("[bold cyan]Stopping the scheduled job...[/]")
            await api.stop_task_api(task_id)

        # Disable task
        console.print("- Scheduled job stopped. Disabling...")
        task_info = await api.disable_task_api(task_id, stop_agent=True)

    if task_info.task_status == TaskStatusEnum.OFF:
        console.print("- Scheduled job disabled. Syncing files...")
        await sync_flow(status, sync_type="task", operations="download")

    console.print("[green]Scheduled job cancelled[/]")
    console.print()

    print_costs(task_info)

    return True


async def stop_flow(status: Status) -> bool:
    """
    Stop Flow - Safely stops running applications and cleans up resources.
    Decision Tree:
    - Lab Application: STOP_AGENT_PROCEDURE
    - API Only Application: STOP_AGENT_PROCEDURE
    - API + Scheduled Job: STOP_TASK_PROCEDURE + STOP_AGENT_PROCEDURE
    - One-time Job: STOP_AGENT_PROCEDURE
    - Scheduled Job: STOP_TASK_PROCEDURE
    """
    status.update("[bold cyan]Stopping application...[/]")
    agent_id = get_agent_id(raise_error=False)
    task_id = get_task_id(raise_error=False)

    job_type = JobTypeEnum(load_config("job_type"))
    job_schedule = load_config("job_schedule")

    # Lab type - always terminate
    if job_type == JobTypeEnum.LAB:
        await stop_agent_flow(status, agent_id)

    # API Only - stop agent
    elif job_type == JobTypeEnum.API and not job_schedule:
        await stop_agent_flow(status, agent_id)

    # API + Scheduled Job - stop both task and agent
    elif job_type == JobTypeEnum.API and job_schedule:
        await stop_task_flow(status, task_id)
        await stop_agent_flow(status, agent_id)

    # Scheduled Job - stop agent and optionally terminate
    elif job_type == JobTypeEnum.JOB and job_schedule:
        await stop_task_flow(status, task_id)

    # One-time Job - stop agent and optionally terminate
    elif job_type == JobTypeEnum.JOB and not job_schedule:
        await stop_agent_flow(status, agent_id)


# HELPERS


async def ask(
    status: Status,
    question: str,
    answers: List[Tuple[str, str]],
    default: Optional[str] = None,
) -> str:
    status.stop()
    select_choices = [Choice(value=answer[0], name=answer[1]) for answer in answers]
    user_choice = await inquirer.select(
        message=question,
        choices=select_choices,
        default=default or select_choices[0].value,
        style=style,
    ).execute_async()
    status.start()

    return user_choice


def make_progress_callback(progress: Progress, task_id: TaskID) -> Callable[[float], None]:
    """Create a progress callback function for tracking file transfer progress."""

    def progress_callback(bytes_transferred: float):
        progress.update(task_id, completed=bytes_transferred)

    return progress_callback


async def inspect_task(task_id: str) -> TaskStatusResponseModel:
    if not task_id:
        return TaskStatusResponseModel(task_id=task_id)

    try:
        return await api.inspect_task_api(task_id)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return TaskStatusResponseModel(task_id=task_id)
        else:
            raise e


async def inspect_agent(agent_id: str) -> AgentStatusResponseModel:
    if not agent_id:
        return AgentStatusResponseModel(agent_id=agent_id)

    try:
        return await api.inspect_agent_api(agent_id)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return AgentStatusResponseModel(agent_id=agent_id)
        else:
            raise e


def get_job_title(job_type: JobTypeEnum) -> str:
    if job_type == JobTypeEnum.JOB:
        return "Job"
    elif job_type == JobTypeEnum.API:
        return "API Service"
    elif job_type == JobTypeEnum.LAB:
        return "Lab (Jupyter Notebook)"


def detect_framework(content: str) -> Tuple[str, str]:
    """
    Detect the framework used in the application and return appropriate commands.

    Args:
        content: Content of main.py file

    Returns:
        Tuple of (framework_name, run_command)
    """
    main_file = "main"
    app_name = "app"
    port = 8008
    host = "0.0.0.0"

    if "from fastapi import" in content:
        return "fastapi", f"python -m uvicorn --host {host} --port {port} {main_file}:{app_name}"
    elif "from flask import" in content:
        return "flask", f"python -m gunicorn -b {host}:{port} -w 3 {main_file}:{app_name}"
    else:
        return "python", f"python {main_file}.py"


async def detect_job_type() -> JobTypeEnum:
    """Detect the job type based on the files in the current directory.

    Returns:
        JobTypeEnum: The job type.
    """
    base_directory = os.getcwd()

    # If requirements.txt exists, add pip install command to build.sh
    requirements_txt_path = os.path.join(base_directory, "requirements.txt")
    build_commands = []
    if os.path.exists(requirements_txt_path):
        build_commands = ["python -m pip install --no-cache-dir -r requirements.txt"]
    save_script("build.sh", build_commands)

    main_py_path = os.path.join(base_directory, "main.py")
    if os.path.exists(main_py_path):
        with open(main_py_path, "r") as f:
            content = f.read()

        # Detect framework and get run command
        framework, run_command = detect_framework(content)

        # Write run command to run.sh
        save_script("run.sh", [run_command])

        if framework in ["fastapi", "flask"]:
            return JobTypeEnum.API
        else:
            return JobTypeEnum.JOB
    else:
        # For LAB type, create empty run.sh
        save_script("run.sh")
        return JobTypeEnum.LAB


def get_environment_variables() -> Dict[str, str]:
    """
    Get environment variables based on env_type config setting.

    Returns:
        Dictionary of environment variables
    """
    env_type = load_config("env_type")
    env_file = load_config("env_file")
    env_values = load_config("env_values", {})

    if not env_type:
        return {}

    if env_type == "file":
        if not env_file:
            console.print("[yellow]Warning: env_type is 'file' but no env_file specified[/]")
            return {}
        return parse_env_file(env_file)
    elif env_type == "values":
        return env_values
    else:
        console.print(f"[yellow]Warning: Unknown env_type '{env_type}'[/]")
        return {}


def parse_env_file(file_path: str) -> Dict[str, str]:
    """
    Parse a .env file and return key-value pairs.

    Args:
        file_path: Path to the .env file

    Returns:
        Dict of environment variable key-value pairs
    """
    env_vars = {}
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split("=", 1)
                if len(parts) == 2:
                    key, value = parts[0].strip(), parts[1].strip()
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    env_vars[key] = value
    except Exception as e:
        console.print(f"[red]Error parsing {file_path}: {str(e)}[/]")

    return env_vars


async def ask_env_var(default: str) -> Tuple[str, str]:
    while True:
        key_value = await inquirer.text(
            message="Environment variable (format: KEY=VALUE):",
            style=style,
            default=default,
        ).execute_async()

        if not key_value:
            return None, None

        parts = key_value.split("=", 1)
        if len(parts) != 2 or not parts[0].strip():
            console.print("[red]Invalid format. Please use KEY=VALUE format.[/]")
        else:
            break

    return parts[0].strip(), parts[1].strip()


async def collect_env_values() -> Dict[str, str]:
    """
    Collect environment variables from user input.

    Args:
        existing_values: Existing environment variables to start with

    Returns:
        Dict of environment variable key-value pairs
    """

    new_values = {}
    old_values = load_config("env_values", {})

    # First, process existing values if any
    if old_values:
        for key, value in old_values.items():
            new_key, new_value = await ask_env_var(f"{key}={value}")
            if new_key is not None:
                new_values[new_key] = new_value

    while True:
        new_key, new_value = await ask_env_var("")
        if new_key is None:
            break
        new_values[new_key] = new_value

    return new_values


def get_task_id(raise_error: bool = True) -> str:
    task_id = load_config("task_id")
    if not task_id:
        if raise_error:
            console.print("[bold red]No task found[/]")
            raise click.Abort()
        else:
            return None
    return task_id


def get_agent_id(raise_error: bool = True) -> str:
    agent_id = load_config("agent_id")
    if not agent_id:
        if raise_error:
            console.print("[bold red]No environment found[/]")
            raise click.Abort()
        else:
            return None
    return agent_id


def print_costs(info: Union[AgentStatusResponseModel, TaskStatusResponseModel]):
    if info.compute_cost is not None or info.storage_cost is not None:
        console.print()
        console.print("[bold]Billing:[/]")
    if info.compute_cost is not None:
        console.print(f"Compute: ${info.compute_cost:.4f}")
    if info.storage_cost is not None:
        console.print(f"Storage: ${info.storage_cost:.4f}")


def print_logs(title: str, logs: List[str]):
    if not logs:
        return

    indent = " " * 4
    console.print(f"{title.title()}:")
    if len(logs) > 0:
        console.print(indent + "...", highlight=False, markup=False)
    for line in logs:
        console.print(indent + line.strip(), highlight=False, markup=False)


def display_environment_variables(env_vars: Dict[str, str], header: str = None) -> None:
    """
    Display environment variables with masked values for sensitive information.

    Args:
        env_vars: Dictionary of environment variables
        header: Optional header text to display before variables
    """
    if not env_vars:
        console.print("[yellow]No environment variables defined.[/]")
        return

    if header:
        console.print(f"[cyan]{header}[/]")

    for key, value in env_vars.items():
        # Mask sensitive values
        masked_value = value[:3] + "****" if len(value) > 6 else "****"
        console.print(f"  {key}={masked_value}")


def validate_cron_format(cron_string: str) -> bool:
    """
    Validate if a string is in proper cron format.

    Args:
        cron_string: The cron string to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        croniter(cron_string, datetime.now())  # Try parsing the cron expression
        return True
    except ValueError:
        return False


def validate_config(config: dict) -> bool:
    """
    Validate configuration
    Returns True if valid, raises ValueError with description if invalid.
    """
    job_type = config.get("job_type")
    job_schedule = config.get("job_schedule")
    compute_size = config.get("compute_size")
    disk_size = config.get("disk_size")
    # storage = config.get("storage")

    # Common validations
    if not compute_size:
        raise ValueError("compute_size is required for all application types")
    if not disk_size:
        raise ValueError("disk_size is required for all application types")
    # if not storage:
    #     raise ValueError("storage configuration is required for all application types")

    # Type-specific validations
    if job_type == JobTypeEnum.LAB.value:
        if job_schedule:
            raise ValueError("job_schedule must be empty for Lab applications")

    elif job_type == JobTypeEnum.API.value:
        # job_schedule is optional for API type
        if job_schedule and not validate_cron_format(job_schedule):
            raise ValueError(
                "If provided, job_schedule must be in cron format for API applications"
            )

    elif job_type == JobTypeEnum.JOB.value:
        if job_schedule and not validate_cron_format(job_schedule):
            raise ValueError(
                "job_schedule must be either empty or in cron format for Job applications"
            )

    else:
        raise ValueError(f"Invalid job_type: {job_type}")

    return True


if __name__ == "__main__":
    cli()
