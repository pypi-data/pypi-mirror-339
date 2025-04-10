from arqsim import stop_and_wait, arq_sim

def test_stop_and_wait():
    print("Testing Stop-and-Wait")
    # Just checking it runs — user interaction required
    try:
        stop_and_wait()
    except Exception as e:
        print(f"❌ Stop-and-Wait failed: {e}")

def test_gbn():
    print("Testing Go-Back-N")
    try:
        arq_sim(win_size=4, rtt=0.5, loss=0.1, ack_loss=0.1, mode="GBN")
    except Exception as e:
        print(f"❌ GBN failed: {e}")

def test_sr():
    print("Testing Selective Repeat")
    try:
        arq_sim(win_size=4, rtt=0.5, loss=0.1, ack_loss=0.1, mode="SR")
    except Exception as e:
        print(f"❌ SR failed: {e}")

if __name__ == "__main__":
    test_gbn()
    test_sr()
