# SAF_ROB4_440_26_Mini_Project

## Procedure

Install the GitHub repo:

```
git clone https://github.com/CasKK/SAF_ROB4_440_26_Mini_Project.git
```

Then, go to the specified folder:

```
cd SAF_ROB4_440_26_Mini_Project/SAF_440_ws
```

Build a docker image...

```
docker build -t miniproject:latest .
```

... and then run this command

```
docker run --rm -it \
  -v "$(pwd)":/ros2_ws \
  -p 12343:12343 \
  miniproject:latest /bin/bash
```

To run the docker again, go to the specified folder and type in the above command.
