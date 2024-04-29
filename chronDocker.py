import schedule
import time
import subprocess
import argparse
import logging

def start_docker_container(container_id):
    logging.info("Starting docker container...")
    subprocess.run(["docker", "start", container_id])

def stop_docker_container(container_id):
    logging.info("Stopping docker container...")
    subprocess.run(["docker", "stop", container_id])

def main(activate_time, deactivate_time, container_id):
    activate_hour, activate_minute = map(int, activate_time.split(":"))
    deactivate_hour, deactivate_minute = map(int, deactivate_time.split(":"))

    schedule.every().day.at(f"{activate_hour:02d}:{activate_minute:02d}").do(lambda: start_docker_container(container_id))

    schedule.every().day.at(f"{deactivate_hour:02d}:{deactivate_minute:02d}").do(lambda: stop_docker_container(container_id))

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
    logging.info("Docker start&stop!\n")

    parser = argparse.ArgumentParser(description="Start & Stop Docker container at specific time")
    parser.add_argument("--start-time", help="Start time of docker container in format HH:MM")
    parser.add_argument("--stop-time", help="Stop time of docker container in format HH:MM")
    parser.add_argument("--container-id", help="Container ID")
    args = parser.parse_args()
    
    logging.info(f"Docker container {args.container_id} will start at {args.start_time} and stop at {args.stop_time}")
    main(args.start_time, args.stop_time, args.container_id)