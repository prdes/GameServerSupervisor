import a2s

# games tested by library author 
# Half-Life 2, Half-Life, Team Fortress 2, Counter-Strike: Global Offensive,
#  Counter-Strike 1.6, ARK: Survival Evolved, Rust


def a2s_query(ip, port):
    address = (ip, port)
    info = a2s.info(address)
    return info

