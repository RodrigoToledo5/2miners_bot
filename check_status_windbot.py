#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
<<<<<<< HEAD
check_status_windbot.py is a bot for check status from https://etc.2miners.com/
=======
"""

import logging
import time
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext,CallbackQueryHandler
import requests as req


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
with open('token.txt','r') as file:
	token=file.read().replace('\n','') 
with open('wallet.txt','r') as file:
	wallet=file.read().replace('\n','') 

def start(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command"""
	update.message.reply_text('Wellcome to check_status_windbot')
	update.message.reply_text('send /help for more information') 

def check_status(update, context):
	keyboard = [
	[
		InlineKeyboardButton("24hs Number Rewards", callback_data='1'),
		InlineKeyboardButton("24hs Reward", callback_data='2'),
	],
	[
		InlineKeyboardButton("Current Hash rate", callback_data='3'),
		InlineKeyboardButton("Current Luck", callback_data='4'),
	],
	[
		InlineKeyboardButton("Average Hash rate", callback_data='5'),
		InlineKeyboardButton("Payment Total", callback_data='6'),
	],
	[
		InlineKeyboardButton("Stats", callback_data='7'),
		InlineKeyboardButton("Total Mature and Uncle", callback_data='8'),
	],
	[
		InlineKeyboardButton("Average Uncle/Mature %", callback_data='9')
	],
	]

	reply_markup = InlineKeyboardMarkup(keyboard)

	update.message.reply_text('What do u need know? :3', reply_markup=reply_markup)

def button(update, context):
	query = update.callback_query
	# CallbackQueries need to be answered, even if no notification to the user is needed
	# Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
	query.answer()
	query.edit_message_text('Checking')
	if query.data=='1':
		numreward(query, context)
	if query.data=='2':
		reward(query, context)
	if query.data=='3':
		current_hash_rate(query,context)
	if query.data=='4':
		currentLuck(query, context)
	if query.data=='5':
		hashrate(query, context)
	if query.data=='6':
		paymentsTotal(query, context)
	if query.data=='7':
		stats(query, context)
	if query.data=='8':
		total_mature(query, context)
		query.message.reply_text('Done :3')
		total_uncle(query, context)
	if query.data=='9':
		query.message.reply_text('Average :'+str(round(uncle_mature(),5)*100)+'%')
		query.message.reply_text('Done :3')

def help_command(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command"""
	update.message.reply_text('/start ')
	update.message.reply_text('/check_status') 

def numreward(update, context):
	url="https://etc.2miners.com/api/accounts/"+str(wallet)
	response=req.get(url)
	if response.status_code==200:
		payload=response.json()
		results=payload.get('24hnumreward')
		update.edit_message_text("24hnumreward: "+str(results))
		update.message.reply_text('Done :3')  
	else :
		update.message.reply_text(str(response))

def reward(update, context):
	url="https://etc.2miners.com/api/accounts/"+str(wallet)
	response=req.get(url)
	if response.status_code==200:
		payload=response.json()
		results=payload.get('24hreward')
		update.edit_message_text('24hs reward: '+str(round((results/1000000000),6))+' ETC')
		update.message.reply_text('Done :3')  
	else :
		update.message.reply_text(str(response))

def current_hash_rate(update, context):
	url="https://etc.2miners.com/api/accounts/"+str(wallet)
	response=req.get(url)
	if response.status_code==200:
		payload=response.json()
		results=payload.get('currentHashrate')
		update.edit_message_text("Current Hash rate: "+str(round((results/1000000),2))+' MH/s')
		update.message.reply_text('Done :3')  
	else :
		update.message.reply_text(str(response))

def currentLuck(update, context):
	url="https://etc.2miners.com/api/accounts/"+str(wallet)
	response=req.get(url)
	if response.status_code==200:
		payload=response.json()
		results=payload.get('currentLuck')
		update.edit_message_text("current Luck: "+str(results))
		update.message.reply_text('Done :3')  
	else :
		update.message.reply_text(str(response))

def hashrate(update, context):
	url="https://etc.2miners.com/api/accounts/"+str(wallet)
	response=req.get(url)
	if response.status_code==200:
		payload=response.json()
		results=payload.get('hashrate')
		update.edit_message_text("Hash rate: "+str(round((results/1000000),2))+' MH/s')
		update.message.reply_text('Done :3')  
	else :
		update.message.reply_text(str(response))

def paymentsTotal(update, context):
	url="https://etc.2miners.com/api/accounts/"+str(wallet)
	response=req.get(url)
	if response.status_code==200:
		payload=response.json()
		results=payload.get('paymentsTotal')
		update.edit_message_text("Payments Total: "+str(results))
		update.message.reply_text('Done :3')  
	else :
		update.message.reply_text(str(response))

def stats(update, context):
	url="https://etc.2miners.com/api/accounts/"+str(wallet)
	response=req.get(url)
	if response.status_code==200:
		payload=response.json()
		results=payload.get('stats')
		update.edit_message_text('Stats:')			
		update.message.reply_text("Balance: "+str(results.get('balance')))
		update.message.reply_text("Blocks Found: "+str(results['blocksFound']))
		update.message.reply_text("Immature "+str(results["immature"]))
		update.message.reply_text("Last Share :"+str(results["lastShare"]))
		update.message.reply_text("Paid :"+str(results["paid"]))
		update.message.reply_text("Pending :"+str(results["pending"]))
		update.message.reply_text('Done :3')  
	else :
		update.message.reply_text(str(response))

def count_mature():
	url="https://etc.2miners.com/api/accounts/"+str(wallet)
	response=req.get(url)
	if response.status_code==200:
		payload=response.json()
		count=0
		results=payload.get('rewards')
		for mature in results:
			if mature["immature"]==False:
				count=count+1			
		return count
	else :
		update.message.reply_text(str(response))

def count_uncle():
	url="https://etc.2miners.com/api/accounts/"+str(wallet)
	response=req.get(url)
	if response.status_code==200:
		payload=response.json()
		count=0
		results=payload.get('rewards')
		for uncle in results:
			if uncle["uncle"]==True:
				count=count+1			
		return count
	else :
		update.message.reply_text(str(response))


def total_mature(update, context):
	url="https://etc.2miners.com/api/accounts/"+str(wallet)
	response=req.get(url)
	if response.status_code==200:
		update.edit_message_text('Total mature: '+str(count_mature()))  
	else :
		update.message.reply_text(str(response))

def total_uncle(update, context):
	url="https://etc.2miners.com/api/accounts/"+str(wallet)
	response=req.get(url)
	if response.status_code==200:
		update.message.reply_text('Total uncle: '+str(count_uncle()))  
	else :
		update.message.reply_text(str(response))

def uncle_mature():
	return count_uncle()/count_mature()

def main():
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater(token, use_context=True)

	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher

    	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("help", help_command))
	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(CommandHandler("check_status", check_status))
	dispatcher.add_handler(CallbackQueryHandler(button))

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

if __name__ == '__main__':
	main()

