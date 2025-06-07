# R_BAAN 🛡️  
> Reconnaissance tool for Bug Bounty Automation

`R_BAAN` is a Python-based automation script that orchestrates the best recon tools — including Subfinder, httpx, GAU, LinkFinder, Arjun, Nuclei, and GoWitness — into one efficient recon workflow for bug bounty hunters.



## ⚙️ Prerequisites

Before running `R_BAAN`, install the following tools and make sure they’re in your system `PATH`:

- [`subfinder`](https://github.com/projectdiscovery/subfinder)
- [`httpx`](https://github.com/projectdiscovery/httpx)
- [`gau`](https://github.com/lc/gau)
- [`LinkFinder`](https://github.com/GerbenJavado/LinkFinder)
- [`Arjun`](https://github.com/s0md3v/Arjun)
- [`nuclei`](https://github.com/projectdiscovery/nuclei)
- [`gowitness`](https://github.com/sensepost/gowitness)

> You can install most of them via `go install`, `pip`, or cloning from GitHub.



## 📦 Installation & Usage

```bash
# Clone the repo
git clone https://github.com/Believer2722/R_BAAN.git
cd R_BAAN

# Run the script (Python 3 required)
python3 main.py -d example.com
