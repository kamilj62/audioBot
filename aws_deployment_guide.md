# AWS Free Tier Deployment Guide (Audio-Bot)

This guide explains how to host your Audio-Bot on AWS for **$0/month** using the AWS Free Tier.

## Prerequisites
- An AWS Account (New accounts get 12 months free).
- Your `OPENAI_API_KEY`.

---

## Step 1: Launch a Free Instance (EC2)

1. Log in to the [AWS Management Console](https://console.aws.amazon.com/).
2. Search for **EC2** and click **Launch Instance**.
3. **Name:** `Audio-Bot-Server`
4. **OS:** Select **Ubuntu** (22.04 or 24.04 LTS).
5. **Instance Type:** Select **t2.micro** (Look for the "Free tier eligible" badge).
6. **Key Pair:** Create a new key pair, download the `.pem` file, and keep it safe.
7. **Network Settings:** 
   - Allow SSH traffic (Port 22).
   - Allow HTTP traffic (Port 80).
8. Click **Launch Instance**.

---

## Step 2: Connect to your Server

Open your terminal (on your Mac) and run:
```bash
chmod 400 your-key.pem
ssh -i "your-key.pem" ubuntu@your-instance-public-ip
```

---

## Step 3: Install Docker & Setup Memory Protection

Once logged into your AWS server, run these commands to install Docker and set up **Swap Space** (this prevents the 1GB RAM from crashing):

```bash
# 1. Setup Swap Space (2GB)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 2. Install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
# Log out and log back in for docker permissions to take effect
exit
```

---

## Step 4: Deploy the Bot

1. **Upload your files** to the server (or clone your repo if you have one on GitHub).
   - From your local machine:
     ```bash
     scp -i "your-key.pem" -r ./Audio-Bot ubuntu@your-instance-public-ip:~/
     ```
2. **Log back in** to the server:
   ```bash
   ssh -i "your-key.pem" ubuntu@your-instance-public-ip
   ```
3. **Create a `.env` file** on the server:
   ```bash
   cd Audio-Bot
   nano .env
   ```
   Paste your keys:
   ```env
   OPENAI_API_KEY=your_actual_key_here
   USE_LOCAL_WHISPER=False
   ```
   (Press `Ctrl+O`, `Enter`, `Ctrl+X` to save).

4. **Start the Bot:**
   ```bash
   sudo docker-compose up -d --build
   ```

---

## Troubleshooting

- **Out of Memory:** If the build fails on the server, build the image on your computer first, push it to **Docker Hub** or **AWS ECR**, and then pull it on the server.
- **Port 80:** The bot is configured to run on Port 80. You can access it in your browser at: `http://your-instance-public-ip`

> [!IMPORTANT]
> **Why is it free?**
> The `t2.micro` is part of the 12-month free tier. By using `USE_LOCAL_WHISPER=False`, we offload the heavy work to OpenAI's API, allowing the bot to run comfortably on this tiny free server.
