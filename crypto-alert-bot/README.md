# Ultimate Forex Frontiers Crypto Alert Bot

A production-ready Telegram bot that automatically posts crypto prices, market news, trending coins, and alerts to your Telegram channel 24/7.

## Features

✅ **Automatic Price Updates** - BTC, ETH, SOL, XRP every 5 minutes
✅ **Top 10 Trending Coins** - Updated every 10 minutes
✅ **Top Gainers & Losers** - Updated every 15 minutes
✅ **Crypto News** - Latest news every 20 minutes
✅ **Fear & Greed Index** - Daily at 08:00 UTC
✅ **Daily Market Summary** - Every 6 hours
✅ **Beautiful Formatting** - Rich emoji and markdown messages
✅ **24/7 Hosting** - Deploy free on Render
✅ **Error Handling** - Automatic retry with exponential backoff
✅ **Logging** - Comprehensive logging to file and console

## Tech Stack

- **Python** 3.12+
- **python-telegram-bot** - Telegram Bot API
- **APScheduler** - Task scheduling
- **requests** - HTTP client
- **python-dotenv** - Environment variables
- **Render** - Cloud hosting

## Project Structure

```
crypto-alert-bot/
├── bot.py              # Main bot entry point
├── config.py           # Configuration and environment loading
├── scheduler.py        # APScheduler setup
├── services/
│   ├── coingecko.py   # Trending coins, gainers/losers
│   ├── cryptopanic.py # Crypto news
│   ├── fear_greed.py  # Fear & Greed Index
│   ├── formatter.py   # Message formatting
│   └── telegram_sender.py  # Telegram message sending
├── utils/
│   ├── logger.py      # Logging setup
│   ├── helpers.py     # Helper functions
│   └── constants.py   # Constants
├── .env               # Environment variables (not in repo)
├── .env.example       # Example environment variables
├── requirements.txt   # Python dependencies
├── render.yaml        # Render deployment config
└── README.md         # This file
```

## Installation

### Prerequisites

- Python 3.12 or higher
- pip package manager
- A Telegram Bot Token (from @BotFather)
- A Telegram Channel ID

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/crypto-alert-bot.git
   cd crypto-alert-bot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Copy and configure .env**
   ```bash
   cp .env.example .env
   ```

5. **Update .env with your credentials**
   ```env
   BOT_TOKEN=your_telegram_bot_token
   CHANNEL_ID=your_channel_id
   CRYPTOPANIC_API_KEY=your_api_key_optional
   ```

6. **Run the bot**
   ```bash
   python bot.py
   ```

## Configuration

Edit `.env` to customize:

```env
# Telegram
BOT_TOKEN=your_token_here
CHANNEL_ID=your_channel_id

# API Keys
CRYPTOPANIC_API_KEY=optional

# Scheduler intervals (minutes)
PRICE_INTERVAL_MINUTES=5
NEWS_INTERVAL_MINUTES=10
SUMMARY_INTERVAL_HOURS=6
FEARGREED_SCHEDULE=08:00  # HH:MM UTC
```

## Getting Your Credentials

### Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow the prompts to create a bot
4. Copy the bot token

### Channel ID

1. Create a Telegram channel
2. Add your bot as an administrator
3. Send a message to the channel
4. Use this URL to get the channel ID:
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
5. Look for the `chat` → `id` field (it starts with a minus sign)

## Deployment on Render

### Step-by-Step

1. **Create a Render Account**
   - Go to https://render.com
   - Sign up and connect your GitHub account

2. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/crypto-alert-bot.git
   git push -u origin main
   ```

3. **Create a Web Service on Render**
   - Go to Render Dashboard
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repo
   - Set environment variables:
     - `BOT_TOKEN`
     - `CHANNEL_ID`
     - `CRYPTOPANIC_API_KEY` (optional)
   - Select Python environment
   - Build: `pip install -r requirements.txt`
   - Start: `python bot.py`
   - Click "Create Web Service"

4. **Monitor Logs**
   - Check the Logs tab in Render dashboard
   - You'll see startup message in your Telegram channel

## Scheduled Tasks

- **Every 5 minutes**: Price updates (BTC, ETH, SOL, XRP)
- **Every 10 minutes**: Trending coins
- **Every 15 minutes**: Top gainers & losers
- **Every 20 minutes**: Crypto news
- **Every 6 hours**: Daily market summary
- **08:00 UTC daily**: Fear & Greed Index

## API Sources

- **Binance**: Cryptocurrency prices
- **CoinGecko**: Trending coins, market data
- **CryptoPanic**: Crypto news
- **Alternative.me**: Fear & Greed Index

## Troubleshooting

### Bot not sending messages

1. Verify `BOT_TOKEN` is correct
2. Verify `CHANNEL_ID` is correct
3. Ensure bot is added as admin to the channel
4. Check logs: `tail -f logs/app.log`

### API errors

1. Check internet connection
2. Verify API endpoints are accessible
3. Check rate limits (some APIs have limits)

### Render deployment issues

1. Check build logs for errors
2. Verify environment variables are set
3. Check Python version matches (3.12+)
4. Restart the web service

## Future Improvements

- [ ] Database: Portfolio tracking
- [ ] Price alerts: Custom price notifications
- [ ] AI summaries: Market analysis
- [ ] Whale alerts: Large transaction tracking
- [ ] User commands: `/price`, `/news`, `/trending`
- [ ] Premium features: Advanced analytics
- [ ] Multi-channel support
- [ ] Export to CSV/Excel

## License

MIT License - See LICENSE file

## Support

For issues and questions:
1. Check the README
2. Review logs in `logs/app.log`
3. Create an issue on GitHub

## Donation

If you find this bot useful, consider supporting the project:
- Follow @ULTIMATEFOREXFRONTIERS on Telegram
- Star the repository
- Share with others

---

**Happy Trading! 🚀**

