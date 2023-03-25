#!/bin/bash

#TODO add venv setup

sudo useradd -r disnake
sudo cp gentlemen.service /etc/systemd/system/
sudo systemctl daemon-reload

sudo systemctl enable gentlemen.service
sudo systemctl start gentlemen.service