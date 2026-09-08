import socket
import random
import argparse
import time
import common

parser = argparse.ArgumentParser()

parser.add_argument("--file", type=str, default="out.bmp", help="Archivo a guardar")
parser.add_argument("--delay", type=float, default=0.0, help="Simula un delay al enviar frames (tanto de emisor como de receptor)")
parser.add_argument("--loss", type=float, default=0.01, help="Probabilidad de pérdida de un frame")

args = parser.parse_args()
out_filename = args.file

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 12002))
last_seq = -1

with open(out_filename, "wb") as out:
    while True:
        raw_data, addr = sock.recvfrom(common.SLIDINGWINDOW_DATA_FRAME_SIZE)
        time.sleep(args.delay)
        (is_last, seq, data) = common.decode_slidingwindow_data_frame(raw_data)

        if random.random() < args.loss:
            print(f"Simulando perdida de frame de datos")
            continue

        if seq <= last_seq:
            # Este frame ya lo habíamos guardado. Ackeo porque el cliente no sabe que lo tengo.
            should_save_data = False
        elif seq == last_seq + 1:
            # Es exactamente el que quiero
            should_save_data = True 
            last_seq = seq 
        else:
            # No quiero ackear un frame del futuro
            continue
            
        ack_frame = common.encode_slidingwindow_ack_frame(last_seq)

        if random.random() < args.loss:
            print(f"Simulando perdida de frame de acknowledgement")
        else:
            sock.sendto(ack_frame, addr)
            time.sleep(args.delay)
            
        if not should_save_data:
            continue

        out.write(data)
        out.flush()

        if is_last:
            print("ultimo frame -> terminamos")
            break

print(f"Descarga guardada en {out_filename}")
sock.close()
