# A Bot to Book Badminton Courts

## How to install

- Just download this Project to your computer.

## Instructions
- To run the program: 
  - For **macOS**
    - Go to the `output` folder/directory (in Terminal)
    - Please run this command to book badminton courts: `./main <day> <time>`
      - For example `./main 3 15` (if I want to book a court at 15:00 on the day after tomorrow) (Normal booking)
      - For example `./main 8 7` (if I want to book a court at 7:00 for today one week later) (Use this to rob a court.)
  - For **windows OS**
    - Go to the `dist` folder/directory (in cmd)
    - Please run this command to book badminton courts: `main.exe <day> <time>`
      - For example `main.exe 0 15` (if I want to book a court at 15:00 today) (Normal booking)
      - For example `main.exe 8 7` (if I want to book a court at 7:00 for today one week later) (Use this to rob a court.)
  - Go to the booking page. (See the following gif)
    - ![book](https://github.com/fb1n15/Gym-Booking-Bot/blob/manual_login/resources/ezgif.com-gif-maker.gif)
- To login from the gym website
  - added `-y` after the command
  - e.g., `main.exe 8 19 -y` (**windows OS**)
- Please start the program after 05:00 and before 00:00. 
- The program will try to book a court at that time (any court) until 00:10 the next day.
- Please reach out to me if there are any bugs. (There should be many. 😹)

## Create Executables (for my reference)
### Create windows executable
- `pyinstaller --onefile main.py`
- [Source](https://datatofish.com/executable-pyinstaller/)

## TODOs
- Login from https://soton.leisurecloud.net/Connect/mrmlogin.aspx
