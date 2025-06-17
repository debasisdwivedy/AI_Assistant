def python_execute(execute_code:str,install_pkg:list)->str:
    """
    Tool: Python virtual environment to execute python code

        Name : python_execute

        Description:
            This tool is used to execute python code and return back the result.
            The result could be of any datatype including Exception string.
            ALWAYS PRINT THE FINAL RESULT.   

        Args:
            execute_code:str = The code that needs to be executed.
            install_pkg:list = The packages that needs to be installed to run the code successfully.

        Usage:
            Call this tool upon receiving a python code and return back the result as a string.

        Output:
            
            result:str = The result from the function call
    """
    import io,uuid
    try:
        import docker
    except ImportError as e:
        raise ImportError("You must install package `docker` to run this tool: for instance run `pip install docker`.") from e

    pkg = " ".join(install_pkg)

    try:
        client = docker.from_env()
    except Exception as e:
        raise Exception("Please make sure the docker deamon is running!!!!",e)

    image_name = str(uuid.uuid4()) #"python-runner"

    dockerfile_str = '''
    FROM python:3.13-slim

    # Create a non-root user and group
    RUN addgroup --system appuser && adduser --system --ingroup appuser appuser

    WORKDIR /app

    # Create virtual environment and install packages there
    RUN python -m venv /venv \
        && . /venv/bin/activate \
        && pip install --no-cache-dir {}

    # Change to non-root user
    USER appuser
    '''.format(pkg)

    # Build image using an in-memory file (BytesIO)
    image, logs = client.images.build(
        fileobj=io.BytesIO(dockerfile_str.encode('utf-8')),
        tag=image_name,
        rm=True,
        pull=False,
        custom_context=False,
        encoding="utf-8"
    )

    # for chunk in logs:
    #     print(chunk.get('stream', ''))

    # Run a container
    container = client.containers.run(
        image=image_name,
        command=["python3", "-c", execute_code],
        security_opt=["no-new-privileges:true"],
        user="appuser",  # run as non-root user
        environment={"PATH": "/venv/bin:$PATH"},  # activate venv
        remove=True,         # Automatically remove container after it exits
        stdout=True,
        stderr=True
    )

    # Output from container
    result = container.decode('utf-8')
    #print(result)


    # Step 1: Remove the image
    try:
        client.images.remove(image=image_name, force=True)
        #print(f"Removed image: {image_name}")
    except docker.errors.ImageNotFound:
        print(f"Image '{image_name}' not found.")
    except docker.errors.APIError as e:
        print(f"Failed to remove image: {e}")

    # Step 2: Prune unused images
    prune_result = client.images.prune()
    #print("Pruned unused images:", prune_result)

    return result





# execute_code= '\ndef fibonacci(n):\n    fib_sequence = [0, 1]\n    while len(fib_sequence) < n:\n        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])\n    return fib_sequence\n\n# Calculate Fibonacci series for 23 numbers\nprint(fibonacci(23))\n'
# install_pkg = ["numpy","pandas"]

# result=python_execute(execute_code,install_pkg)
# print(result)