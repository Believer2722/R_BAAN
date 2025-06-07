import os
import subprocess

def run_command(command, description):
    print(f"\n[*] {description}...")
    print(f"[+] Running: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Skipping {description}: {e}")

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def ask_to_run(tool_name):
    choice = input(f"\n[?] Run {tool_name}? [Y/n]: ").strip().lower()
    return choice in ["", "y", "yes"]

def print_header():
    print(r"""
  ____    ____      _        _    __   __     
 |  _ \  | __ )    / \      / \   | | | | 
 | |_) | |  _ \   / _ \    / _ \  |  \| |
 |  _ <| | |_) | / ___ \  / ___ \ | |\  |
 |_| \_\ |____/ /_/   \_\/_/   \_\\_| \_|

    [ R_BAAN Recon Tool – Combination of Multiple Tools ]
    """)

def main():
    print_header()
    domain = input("Enter the target domain: ").strip()
    output_dir = f"output/{domain}"
    create_dir(output_dir)

    subs_file = f"{output_dir}/subs.txt"
    live_file = f"{output_dir}/live.txt"
    urls_file = f"{output_dir}/urls.txt"
    js_endpoints = f"{output_dir}/js_endpoints.txt"
    arjun_input = f"{output_dir}/arjun_input.txt"
    arjun_output = f"{output_dir}/arjun_output.txt"

    # === Subfinder ===
    if ask_to_run("Subfinder"):
        run_command(
            f"subfinder -d {domain} -o {subs_file}",
            "Subdomain Enumeration using Subfinder"
        )
    else:
        print("[*] Skipping Subfinder.")

    # === Httpx ===
    if ask_to_run("Httpx"):
        if os.path.exists(subs_file) and os.path.getsize(subs_file) > 0:
            run_command(
                f"cat {subs_file} | httpx -silent > {live_file}",
                "Checking live hosts with httpx"
            )
        else:
            print("[!] Skipping httpx: subs.txt not found or empty.")
    else:
        print("[*] Skipping Httpx.")

    # === GAU ===
    if ask_to_run("GAU (GetAllUrls)"):
        run_command(
            f"gau {domain} --o {urls_file}",
            "Collecting URLs using gau"
        )
    else:
        print("[*] Skipping GAU.")

    # === LinkFinder ===
    if ask_to_run("LinkFinder"):
        if os.path.exists(urls_file) and os.path.getsize(urls_file) > 0:
            run_command(
                f"grep '.js' {urls_file} | while read url; do python3 ~/LinkFinder/linkfinder.py -i \"$url\" -o cli >> {js_endpoints}; done",
                "Extracting JS endpoints with LinkFinder"
            )
        else:
            print("[!] Skipping LinkFinder: urls.txt not found or empty.")
    else:
        print("[*] Skipping LinkFinder.")

    # === Arjun ===
    if ask_to_run("Arjun"):
        if os.path.exists(urls_file) and os.path.getsize(urls_file) > 0:
            run_command(
                f"grep '=[^&]' {urls_file} | sort -u > {arjun_input}",
                "Extracting parameter URLs for Arjun"
            )
            run_command(
                f"arjun -i {arjun_input} -oT {arjun_output} -t 10 -d 0.2 --stable --disable-redirects",
                "Running Arjun for parameter discovery"
            )
        else:
            print("[!] Skipping Arjun: urls.txt not found or empty.")
    else:
        print("[*] Skipping Arjun.")

    # === Nuclei ===
    if ask_to_run("Nuclei"):
        if os.path.exists(live_file) and os.path.getsize(live_file) > 0:
            run_command(
                f"nuclei -l {live_file} -o {output_dir}/nuclei.txt",
                "Running nuclei sfor vulnerability scanning"
            )
        else:
            print("[!] Skipping Nuclei: live.txt not found or empty.")
    else:
        print("[*] Skipping Nuclei.")

    # === GoWitness ===
    if ask_to_run("GoWitness"):
        if os.path.exists(live_file) and os.path.getsize(live_file) > 0:
            gowitness_output_dir = f"{output_dir}/screenshots"
            create_dir(gowitness_output_dir)
            run_command(
                f"gowitness scan file -f {live_file} -s {gowitness_output_dir}"
                f" --chrome-path /usr/bin/chromium",
                "Running gowitness for screenshots"
            )
        else:
            print("[!] Skipping GoWitness: live.txt not found or empty.")
    else:
        print("[*] Skipping GoWitness.")

    print("\n✅ Recon Completed.")

if __name__ == "__main__":
    main()
