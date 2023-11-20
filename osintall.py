import argparse
import yaml
import asyncio
import subprocess
import shutil
import os


async def execute_commands(config, mails, commands, output_dir):
    tasks = []

    for command in commands:
        if config[command]:
            command_to_execute = config[command].replace("{{mails}}", mails)
            print("Executing: {}".format(command_to_execute))

            process = await asyncio.create_subprocess_shell(
                command_to_execute, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            tasks.append((command, process.communicate()))

    results = await asyncio.gather(*[task[1] for task in tasks])
    results = zip([task[0] for task in tasks], results)

    for command, result in results:
        stdout, stderr = result
        output_filename = os.path.join(output_dir, f"{command}.txt")

        with open(output_filename, "w") as output_file:
            output_file.write(f"Command Output:\n{stdout.decode()}\n")
            output_file.write(f"Command Error:\n{stderr.decode()}\n")
        print(f"Output saved to: {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--mails", help="File to read mails from", required=True)
    parser.add_argument("--config", help="Config file to use", required=True)
    parser.add_argument(
        "--commands", help="Commands to execute", required=True, nargs="+"
    )
    parser.add_argument(
        "-c",
        "--clean",
        help="Clean output directory",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output directory",
        default="output",
    )
    args = parser.parse_args()

    if args.clean:
        print("Cleaning output directory")
        try:
            shutil.rmtree(args.output)
        except FileNotFoundError:
            pass

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    try:
        with open(args.mails, "r") as f:
            pass
    except IOError:
        print("Error: Could not read mails file")
        exit(1)

    try:
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)
    except IOError:
        print("Error: Could not read config file")
        exit(1)

    for command in args.commands:
        if command not in config:
            print(f"Error: Command {command} not found in config file")
            exit(1)

    asyncio.run(execute_commands(config, args.mails, args.commands, args.output))
