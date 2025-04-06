import mtasanpystatus

def test_server(ip: str, port: int = 22003):
    """Test the lightweight server query library"""
    try:
        print(f"\nConnecting to {ip}:{port}...")
        mtasanpystatus.connect(ip, port)
        
        print("\n=== Server Status ===")
        print(f"Name: {mtasanpystatus.name or 'Unknown'}")
        print(f"Players: {mtasanpystatus.players or 0}/{mtasanpystatus.maxplayers or 0}")
        print(f"Gamemode: {mtasanpystatus.gamemode or 'Unknown'}")
        print(f"Map: {mtasanpystatus.map or 'Unknown'}")
        print(f"Version: {mtasanpystatus.version or 'Unknown'}")
        print(f"Join Link: {mtasanpystatus.join_link or 'Not available'}")
        
    except mtasanpystatus.ServerException as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_server("51.91.215.201", 22003)