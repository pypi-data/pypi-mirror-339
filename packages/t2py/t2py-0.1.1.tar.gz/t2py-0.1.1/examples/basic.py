import t2py
import time

def main():
    # Find Titan Two
    devices = t2py.Titan2.getdisc()
    if not devices:
        print("no Titan Two found! Make sure it's plugged in.")
        return
        
    print(f"found Titan Two at: {devices[0][0]}")
    
    # Connect to it
    t2 = t2py.Titan2()
    if not t2.connect():
        print("Couldn't connect to Titan Two!")
        return
        
    print("connected to Titan Two!")
    print("sending test signal")
    
    try:
        while True:
            t2.sendgvc([1, 100])
            
    except KeyboardInterrupt:
        # Clean up when user hits Ctrl+C
        print("\nStopping...")
        t2.sendgvc([1, 0]) 
        time.sleep(0.5)
        t2.disconnect()
        print("Done!")

if __name__ == "__main__":
    main() 