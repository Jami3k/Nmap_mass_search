import subprocess

while True:
    print("Starting this really cool and handy script... ")

    # defines the scope
    networkips = input("Enter the target IP range or target IP (Press Enter or lh for localhost): ")

    if networkips == "":
        targetips = "127.0.0.1"
    elif networkips.lower() == "lh":
        targetips = "127.0.0.1"
    else:
        targetips = networkips 


    # checks if single-target mode should be applied and asks the user for the requested port or port spray on single target
    if not "-" in targetips and not "," in targetips and not "*" in targetips:
        rawport = input("Enter the target port (Enter top20 for top 20 ports and top200 for the top 200): ")
        if rawport == "top20":
            port = ["--top-ports", "20"]
        elif rawport == "top200":
            port = ["--top-ports", "200"]
        else: 
            port = ["-p", rawport]
    else: 
        rawport = input("Enter the target port: ")
        port = ["-p", rawport]

    # nmap command stored in a variable
    nmap_command = ["nmap"] + port + [targetips]

    # runs the nmap command and stores the result in a variable
    nmap_result = subprocess.run(nmap_command, capture_output=True, text=True)
    # print (nmap_result) # for debugging purposes
    # takes output lines and looks for hostname/ip address
    output_lines = nmap_result.stdout.splitlines()
    ip = None 
    ips_with_open_ports = []

    # initializes open_ports_count
    open_ports_count = 0

    for line in output_lines:
        # checks for a hostname
        if line.startswith("Nmap scan report for"):
            if "(" in line and ")" in line:
                ip = line.split("(")[-1].strip(")")
            else: 
                ip = line.split()[-1] 

        # checks if target port is open and adds to the list or count
        if "open" in line:
            open_ports_count += 1
            
        # checks if target port is open and if so appends the ip-address to the list
        if "open" in line and ip:
            ips_with_open_ports.append(ip) 
    # initializes result variable
    result = ips_with_open_ports
    # output message logic
    if "--top-ports" in port:
        if open_ports_count == 1:
            print(f"\n{ip} has at least one open port. Go check it out!")
        elif open_ports_count == 0:
            print(f"\nIt seems like there were no open target ports found. Dang it, now I've learnt all these fancy techniques for nothing!")
        else:
            print(f"\n{ip} has at least {open_ports_count} open ports. Go check it out!")
    else: 
        if result:
            if len(port) == 2 and not "-" in targetips and not "," in targetips and not "*" in targetips:            
                print("Target port open! Go hack it!")

            else:                
                print("\nAnd the target IP's are... \n")
                for ip in result:
                    print(ip + "\n")           

        else:

            print(f"\nIt seems like there were no open port {rawport}'s found. Dang it, now I've learnt all these fancy techniques for nothing!")
          

    # Ask if the user wants to run the script again
    repeat = input("Do you want to run the script again? (Y/n): ")
    if repeat.lower() != 'y' and repeat.lower() != "":
        print("Exiting this really cool and handy script. Goodbye!" + "\n")
        break

