import b4p 

b4p.init()


print(b4p.EURS)

b4p.Accounts.new("energy provider")
b4p.Accounts.new("energy consumer")

b4p.Market.new("neighborhood","energy provider")
b4p.Market.new("neighborhood2","energy provider")
b4p.Market.new("neighborhood3","energy provider")


b4p.ProducingAsset.new("solar panel", "energy provider", "neighborhood")
b4p.ConsumingAsset.new("house", "energy consumer", "neighborhood2")

b4p.Market.setConnections("neighborhood3","energy provider","neighborhood2", "neighborhood")
