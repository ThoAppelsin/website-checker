Ever wanted to be notified as soon as the content of a web-page changes?
The web-page in question does not support RSS subscription?
This application is here to help.

## What it does

For any given website, it repeatedly checks it for you,
every 5 seconds by default.
If it ever appears to have a different content since the last time it was checked,
it terminates with a warning that the web-site it has been set to check, has been changed.

If you are on Windows, then it also notifies you with a beep sound.
It is likely that this feature will yield an error in other operating systems,
which I plan to fix in the future.

## How to use it

You will first need to install required packages, just for once. However, even before that,
it is recommended for you to set up a virtual environment for it first.

```powershell
# This creates a virtual environment folder called 'env'
python -m venv env

# This one activates the virtual environment
./env/Scripts/activate
```

Then the installation of packages:

```powershell
pip install -r requirements.txt
```

After this setup, you may use it again and again with the following two lines of commands:

```powershell
# Make sure that your virtual environment is active first
./env/Scripts/activate

# Run the script
python WCheck.py
```

From here on, the program should be guiding you how to use it.
