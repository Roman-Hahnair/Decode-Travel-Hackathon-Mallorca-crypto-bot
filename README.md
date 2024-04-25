# Intro

This a fun project for the [Decode Travel Hackathon](https://decode.travel/) and the Mallorca undersea ecology restoration project. 

# High-level explanation of project functionality

It works like this:
- There is a chatbot-based simple game with a real-life component
- The user walks on the beaches of Mallorca and sometimes finds our secret objects with NFCs
- The user scans an unique NFC and recieves a link to our telegram bot, which keeps the count of the unique objects found
- After the user collected a certain amount of objects, they got a special reward: the bot creates an unique pixel art image according to their description
- The user then asked to contribute to the ecology restoration project
- If the user agrees, the bot mints a unique NFT with the image they generated.

See the workflow in the screenshots below.

# Tech overview of codebase

The project combines several cool things:

- chatbots and text-based interfaces 
- generative AI
- physical NFCs
- blockchain and NFTs
- gamification for a good cause.

The codebase is written mostly in Python.

for the interface, we've build a bot in the popular messenger Telegram. The bot is built with the help of the python-telegram-bot library.

For the generative AI, we've used OpenAI's DALL-E model. The model is called via the OpenAI API.

The bot is able to mint NFTs with the help of the web3.py library.

# Architecture

![Screenshot 0](/media/architecture.jpg)


# Screenshots

Below are the screenshots of the workflow:

The bot greats the user:
![Screenshot 0](/media/bot_screenshots/0.png)

The game starts:
![Screenshot 1](/media/bot_screenshots/1.png)

The user has located the first secret code (e.g. by scanning the plaque with the NFC tag or by entering the code manually):
![Screenshot 2](/media/bot_screenshots/2.png)

The user entered another secret code. As the user has collected enough codes, the bot provides a reward: it asks the user to describe the image they want to generate:
![Screenshot 3](/media/bot_screenshots/3.png)

The user wants an image of a funny puppy:
![Screenshot 4](/media/bot_screenshots/4.png)

The bot generates a cool pixel art pictue with the help of OpenAI's DALL-E:
![Screenshot 5](/media/bot_screenshots/5.png)

The bot asks the user to contribute to the ecology restoration project:
![Screenshot 6](/media/bot_screenshots/6.png)

A payment website opens:
![Screenshot 7](/media/bot_screenshots/7.png)

The user pays with the help of MetaMask:
![Screenshot 8](/media/bot_screenshots/8.png)

After the payment, the user is redirected back to the bot, with his public key in the deep link data:
![Screenshot 9](/media/bot_screenshots/9.png)

The bot mints an NFT as a reward:
![Screenshot 10](/media/bot_screenshots/10.png)

The user can see the NFT in the wallet:
![Screenshot 11](/media/bot_screenshots/11.png)


# How to deploy:

0. 

1. Create a VM, and SSH to it.

2. Clone the repository into it: 

```
git clone https://github.com/Roman-Hahnair/Decode-Travel-Hackathon-Mallorca-crypto-bot
```

3. Install the dependencies with pip

cd to the Decode-Travel-Hackathon-Mallorca-crypto-bot dir and run in a terminal:

```
pip install -r requirements.txt
```

4. Specify the API keys like this:

```
echo "export TELEGRAM_BOT_TOKEN='<your_token>'" >> ~/.bashrc

echo "export OPENAI_API_KEY='<your_token>'" >> ~/.bashrc

echo "export CRYPTO_PRIVATE_KEY='<your_token>'" >> ~/.bashrc

source ~/.bashrc
```

5. Run the main script in tmux

```
tmux new -s session_name

python3 main.py
```

To leave the script running even after you log out, press `Ctrl+b`, and then press `d`.

To return to the session in the future, run `tmux attach -t session_name`.

