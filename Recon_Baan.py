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


def main():
    print_header()  # This calls the header-printing function

def print_header():
    print(r"""
  ____    ____      _        _    __   __     
 |  _ \  | __ )    / \      / \   | | | | 
 | |_) | |  _ \   / _ \    / _ \  |  \| |
 |  _ <| | |_) | / ___ \  / ___ \ | |\  |
 |_| \_\ |____/ /_/   \_\/_/   \_\\_| \_|

                [ R_BAAN Recon Tool Combination of Multiple Tools ]
    """)
    
    domain = input("Enter the target domain: ").strip()
    output_dir = f"output/{domain}"
    create_dir(output_dir)

    # Subfinder
    run_command(
        f"subfinder -d {domain} -o {output_dir}/subs.txt",
        "Subdomain Enumeration using Subfinder"
    )

    # Httpx - checking live subdomains
    subs_file = f"{output_dir}/subs.txt"
    live_file = f"{output_dir}/live.txt"
    if os.path.exists(subs_file) and os.path.getsize(subs_file) > 0:
        run_command(
            f"cat {subs_file} | httpx -silent > {live_file}",
            "Checking live hosts with httpx"
        )
    else:
        print("[!] Skipping httpx: subs.txt not found or empty.")

    # gau - collect URLs
    urls_file = f"{output_dir}/urls.txt"
    run_command(
        f"gau {domain} --o {urls_file}",
        "Collecting URLs using gau"
    )

    # LinkFinder - extract JS endpoints
    js_endpoints = f"{output_dir}/js_endpoints.txt"
    if os.path.exists(urls_file) and os.path.getsize(urls_file) > 0:
        run_command(
            f"grep '.js' {urls_file} | while read url; do python3 ~/LinkFinder/linkfinder.py -i \"$url\" -o cli >> {js_endpoints}; done",
            "Extracting JS endpoints with LinkFinder"
        )
    else:
        print("[!] Skipping LinkFinder: urls.txt not found or empty.")

    # Arjun - fast parameter discovery
    arjun_input = f"{output_dir}/arjun_input.txt"
    arjun_output = f"{output_dir}/arjun_output.txt"
    
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

    # nuclei vulnerability scanning
    if os.path.exists(live_file) and os.path.getsize(live_file) > 0:
        run_command(
            f"nuclei -l {live_file} -o {output_dir}/nuclei.txt",
            "Running nuclei for vulnerability scanning"
        )
    else:
        print("[!] Skipping nuclei: live.txt not found or empty.")

    # gowitness screenshots
    if os.path.exists(live_file) and os.path.getsize(live_file) > 0:
        gowitness_output_dir = f"{output_dir}/screenshots"
        create_dir(gowitness_output_dir)
        run_command(
            f"gowitness file -f {live_file} -P {gowitness_output_dir}",
            "Running gowitness for screenshots"
        )
    else:
        print("[!] Skipping gowitness: live.txt not found or empty.")

    print("\n✅ Recon Completed.")

if __name__ == "__main__":
    main()
