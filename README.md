# Testing1


# Useful things to do when debugging: 

# chrome://net-internals/#sockets
# Refreshes sockets when running local.




## How to Resolve Execution Policy Issue for Virtual Environment Activation

If you encounter an issue with the execution policy preventing the activation of the virtual environment using the `activate` script in the `.venv` directory in Windows PowerShell, you can follow these steps to resolve it:

1. Open a new PowerShell window with administrative privileges.
2. Run the following command to allow script execution for the current session:
    ```
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    ```
3. Navigate to your project directory and try running the `activate` script again:
    ```
    .\.venv\Scripts\activate
    ```
   Note that changing the execution policy to "Bypass" may pose a security risk, so it's recommended to restore the original execution policy once you're done with your virtual environment. You can do this by closing the PowerShell window or running the following command:
    ```
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Default
    ```
   If you prefer to bypass the execution policy only for the `activate` script, you can use the `-ExecutionPolicy` parameter with the `powershell` command to specify a different execution policy for a specific script, like this:
    ```
    powershell -ExecutionPolicy Bypass -File .\.venv\Scripts\activate
    ```
   This way, the execution policy will be bypassed only for the `activate` script, and the original execution policy will not be changed.



