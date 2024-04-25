# Intro

This a fun project for the [Decode Travel Hackathon](https://decode.travel/) and the Mallorca undersea ecology restoration project. 

The project combines several cool things:

- chatbots and text-based interfaces
- generative AI
- physical NFCs
- blockchain and NFTs
- gamification for a good cause

It is a simple:
- There is a chatbot-based simple game with a real-life component
- The user walks on the beaches of Mallorca and sometimes finds our secret objects with NFCs
- The user scans an unique NFC and recieves a link to our telegram bot, which keeps the count of the unique objects found
- After the user collected a certain amount of objects, they got a special reward: the bot creates an unique pixel art image according to their description
- The user then asked to contribute to the ecology restoration project
- If the user agrees, they get a unique NFT with the image they generated.

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

