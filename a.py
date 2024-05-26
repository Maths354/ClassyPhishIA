from analyse_phishing.main import Main


allData = Main("https://www.twitch.tv")

print(allData.main()["scores"])