## OpenAI reflection prompts log monitor

The log_monitor_talk_to_activity_server.py script is part of repo:https://github.com/atharva-naik/interactive-reflection-prompts

This script needed to be started once mysql container is up in the session.

The startup command is included in docker-entrypoint.sh on line 428
```
python log_monitor_talk_to_activity_server.py &
```

Thus we also need to replace this file in mysql container before startup.

Using the Dockerfile build a container (on x86 arch machine) and request the ope research team to replace the new docker image in the deployment.
