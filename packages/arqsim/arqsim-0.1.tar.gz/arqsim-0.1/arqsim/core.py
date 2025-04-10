import random, time

def simulate(prob):
    return random.random() < prob

def get_inputs(*args):
    return [float(input(f"{arg}: ")) if "prob" in arg or "time" in arg else int(input(f"{arg}: ")) for arg in args]

def stop_and_wait():
    loss, ack_loss, max_retries, num_packets, size = get_inputs(
        "Packet loss prob (0–1)", "ACK loss prob (0–1)", "Max retransmissions", "Number of packets", "Packet size (bytes)"
    )
    tx, retx, bit_errors = 0, 0, 0

    for pkt in range(1, num_packets + 1):
        for _ in range(max_retries):
            tx += 1
            if simulate(loss):
                print(f"Packet {pkt} lost.")
                retx += 1
                continue
            print(f"Sent Packet {pkt} ({size}B)")
            if simulate(random.random()):
                print(f"Bit error in Packet {pkt}")
                bit_errors += size * 8
                retx += 1
                continue
            if simulate(ack_loss):
                print(f"ACK for Packet {pkt} lost.")
                retx += 1
            else:
                print(f"Packet {pkt} ACK ✅")
                break
        else:
            print(f"Packet {pkt} failed ❌")

    bits = tx * size * 8
    print("\n🔍 Summary:")
    print(f"Total TX: {tx}, Retrans: {retx}, Bit Errors: {bit_errors}")
    print(f"Efficiency: {100*(tx-retx)/tx:.2f}%, Reliability: {100*(num_packets-retx)/num_packets:.2f}%, BER: {100*bit_errors/bits:.5f}%")

def arq_sim(win_size, rtt, loss, ack_loss, mode):
    packets = [f"P{i+1}" for i in range(8 if mode == "SR" else 5)]
    acked = [False] * len(packets)
    sent, base = 0, 0

    while base < len(packets):
        for i in range(base, min(base + win_size, len(packets))):
            if not acked[i]:
                if simulate(loss):
                    print(f"{packets[i]} lost ❌")
                else:
                    print(f"Sent {packets[i]}")
                    sent += 1
        print("Waiting for ACKs...")
        for i in range(base, min(base + win_size, len(packets))):
            if not acked[i]:
                if simulate(ack_loss):
                    print(f"ACK {i+1} lost ❌")
                else:
                    print(f"ACK {i+1} ✅")
                    acked[i] = True
                if mode == "SR":
                    time.sleep(rtt)
        while base < len(packets) and acked[base]:
            base += 1
        if base < len(packets) and mode == "GBN":
            print(f"Timeout → Resend from {base+1}")
            time.sleep(rtt * 2)
    print(f"\nTotal sent: {sent}")
