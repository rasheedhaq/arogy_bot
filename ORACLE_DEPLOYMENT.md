# Oracle Cloud Deployment Guide for ArogyaBot

## Prerequisites
- Oracle Cloud Account (Always Free Tier)
- SSH key pair
- Your bot code on GitHub

## Step 1: Create Oracle Cloud Account
1. Go to https://www.oracle.com/cloud/free/
2. Click "Start for free"
3. Fill in your details (requires credit card for verification, but won't be charged)
4. Verify your email
5. Complete the setup

## Step 2: Create a Compute Instance (VM)

### 2.1 Access Compute Instances
1. Log in to Oracle Cloud Console
2. Click the hamburger menu (☰) → **Compute** → **Instances**
3. Click **Create Instance**

### 2.2 Configure Instance
**Name:** `arogyabot-vm`

**Placement:**
- Availability Domain: (Select any available)

**Image and Shape:**
- **Image:** Ubuntu 22.04 (or latest Ubuntu)
- **Shape:** 
  - Click "Change Shape"
  - Select **VM.Standard.A1.Flex** (ARM-based, Always Free)
  - OCPUs: 1
  - Memory: 6 GB
  - OR use **VM.Standard.E2.1.Micro** (x86, Always Free, 1GB RAM)

**Networking:**
- **VCN:** Create new or use existing
- **Subnet:** Public subnet
- **Assign public IP:** ✅ Yes

**Add SSH Keys:**
- Generate SSH key pair (if you don't have one):
  ```bash
  ssh-keygen -t rsa -b 4096 -f ~/.ssh/oracle_cloud_key
  ```
- Upload the **public key** (.pub file)
- Save the **private key** securely

**Boot Volume:**
- Keep defaults (50 GB is fine)

Click **Create**

## Step 3: Configure Security (Open Ports)

### 3.1 Add Ingress Rules
1. Go to **Networking** → **Virtual Cloud Networks**
2. Click your VCN → **Security Lists** → **Default Security List**
3. Click **Add Ingress Rules**
4. Add these rules:

**For SSH:**
- Source CIDR: `0.0.0.0/0`
- IP Protocol: TCP
- Destination Port: 22

**For Bot (Optional - if you add a web interface later):**
- Source CIDR: `0.0.0.0/0`
- IP Protocol: TCP
- Destination Port: 8000

### 3.2 Configure Ubuntu Firewall
After SSH-ing into the VM:
```bash
sudo ufw allow 22/tcp
sudo ufw allow 8000/tcp
sudo ufw enable
```

## Step 4: Connect to Your VM

Get your VM's public IP from the Oracle Console, then:

```bash
ssh -i ~/.ssh/oracle_cloud_key ubuntu@<YOUR_VM_PUBLIC_IP>
```

## Step 5: Setup the VM

### 5.1 Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 5.2 Install Python and Dependencies
```bash
# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip git

# Install system dependencies
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
```

### 5.3 Clone Your Repository
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/arogy_bot.git
cd arogy_bot

# Switch to the v2 branch
git checkout v2-refactor-improvements
```

### 5.4 Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 5.5 Setup Environment Variables
```bash
nano .env
```

Paste your environment variables:
```env
TELEGRAM_BOT_TOKEN=your_token_here
GROQ_API_KEY=your_groq_key_here
GROQ_MODEL=llama-3.3-70b-versatile
DOCTORS_DB_PATH=data/doctors_clean.csv
DEBUG=false
# Add other API keys as needed
```

Save: `Ctrl+X`, then `Y`, then `Enter`

## Step 6: Create Systemd Service (Auto-start on boot)

### 6.1 Create Service File
```bash
sudo nano /etc/systemd/system/arogyabot.service
```

### 6.2 Add This Configuration
```ini
[Unit]
Description=ArogyaBot Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/arogy_bot
Environment="PATH=/home/ubuntu/arogy_bot/venv/bin"
ExecStart=/home/ubuntu/arogy_bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save: `Ctrl+X`, then `Y`, then `Enter`

### 6.3 Enable and Start Service
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable arogyabot

# Start the service
sudo systemctl start arogyabot

# Check status
sudo systemctl status arogyabot
```

## Step 7: Verify Deployment

### Check if bot is running:
```bash
sudo systemctl status arogyabot
```

### View logs:
```bash
# Live logs
sudo journalctl -u arogyabot -f

# Last 100 lines
sudo journalctl -u arogyabot -n 100
```

### Restart bot:
```bash
sudo systemctl restart arogyabot
```

### Stop bot:
```bash
sudo systemctl stop arogyabot
```

## Step 8: Update Bot Code (Future Updates)

```bash
cd ~/arogy_bot
git pull origin v2-refactor-improvements
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart arogyabot
```

## Troubleshooting

### Bot not starting?
```bash
# Check logs
sudo journalctl -u arogyabot -n 50

# Check if Python process is running
ps aux | grep python

# Test manually
cd ~/arogy_bot
source venv/bin/activate
python main.py
```

### Can't SSH?
- Check Security List has port 22 open
- Check Ubuntu firewall: `sudo ufw status`
- Verify you're using the correct private key
- Check VM is running in Oracle Console

### Out of memory?
- Use the A1.Flex shape (6GB RAM) instead of E2.1.Micro (1GB)
- Or add swap space:
  ```bash
  sudo fallocate -l 2G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
  ```

## Monitoring

### Check disk space:
```bash
df -h
```

### Check memory:
```bash
free -h
```

### Check CPU:
```bash
top
```

## Security Best Practices

1. **Keep system updated:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Use SSH keys only** (disable password auth):
   ```bash
   sudo nano /etc/ssh/sshd_config
   # Set: PasswordAuthentication no
   sudo systemctl restart sshd
   ```

3. **Keep .env file secure:**
   ```bash
   chmod 600 .env
   ```

4. **Regular backups of database:**
   ```bash
   # Backup
   cp data/arogy.db data/arogy.db.backup

   # Or setup automated backups
   crontab -e
   # Add: 0 2 * * * cp /home/ubuntu/arogy_bot/data/arogy.db /home/ubuntu/backups/arogy.db.$(date +\%Y\%m\%d)
   ```

## Cost: $0 Forever! 🎉

Oracle's Always Free tier includes:
- 2 AMD-based Compute VMs (1/8 OCPU, 1GB RAM each)
- OR 4 ARM-based Ampere A1 cores (up to 24GB RAM total)
- 200 GB Block Volume
- 10 GB Object Storage
- **No time limit - truly free forever!**

---

## Quick Reference Commands

```bash
# Start bot
sudo systemctl start arogyabot

# Stop bot
sudo systemctl stop arogyabot

# Restart bot
sudo systemctl restart arogyabot

# Check status
sudo systemctl status arogyabot

# View logs
sudo journalctl -u arogyabot -f

# Update code
cd ~/arogy_bot && git pull && sudo systemctl restart arogyabot
```

---

**Your bot will now run 24/7 on Oracle Cloud for free!** 🚀
