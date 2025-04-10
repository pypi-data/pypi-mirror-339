"""
Version : 1.0
Author  : ammar.jamalakbar@amd.com
Desc    : extract training value for DCA/DCS that is available
"""

import re
import sys
import os
import pandas as pd
import argparse
import glob
import numpy as np
import site
import rd_wr_eye

def get_bios_hostname(base):
    bios = ""
    hostname = ""
    text = base.split("_")
    if len(text)>1:
        bios = text[0]
        hostname = text[1]      
    for item in text:
        if item.startswith("V"):
            bios = item
        if ("congo" in item) or ("morocco" in item):
            hostname = item
    return bios, hostname


def get_files_from_directory(directory):
    """Get all .csv files from the given directory."""
    csv_files = glob.glob(os.path.join(directory, "*.csv*"))
    print(csv_files)
    return csv_files


def detect_decoded_log(filename):


    decoded_pattern = re.compile(rf"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),.*ADDR:\s*(\w+),\s*DATA:\s*(\w+)")
    pattern_rxen = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),.*<< Rank:\s*(\d+),\s*(\w+)"
    )
    pattrn_rd_eye = re.compile(
        'CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),.*Phase\s*0x([0-9A-Fa-f]+),\s*Dbyte\s*0x([0-9A-Fa-f]+),\s*Nibble\s*0x([0-9A-Fa-f]+),\s*Dq\s*0x([0-9A-Fa-f]+),\s*CenterDelay\s*0x([0-9A-Fa-f]+)'
    )
    
    pattern_txen = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),.*<< Rank:\s*(\d+)\s*(\w+\s*\w+\s*\w+)"
    )

    path = site.getsitepackages()[1]
    mapping_file = f"{path}\eddr_scripts\maps\TRAIN_msgblk_addr_map.csv"  
    default_mapping = "\eddr5_addr_train\TRAIN_msgblk_addr_map.csv"

    if not os.path.exists(mapping_file):
        print("Cannot find eddr5 script, loading default mapping")
        path = os.getcwd()
        mapping_file = path + default_mapping
        print(mapping_file)


    dcs_value = {}
    dcs_coarse = {}
    dcs_vref = {}
    dca_value = {}
    dca_coarse = {}
    dca_vref = {}
    wl_value = {}
    wlcoarse_value = {}
    rxen_value = {}
    rxencoarsedly_value = {}
    rxencoarsesel_value = {}
    rxdlyodd_value = {}
    rxdlyeven_value = {}
    rxdlyevenu_value = {}
    rxdlyoddu_value = {}
    rxdlyevenl_value = {}
    rxdlyoddl_value = {}  
    rxvref_value = {}
    txvref_value= {}
    rxvref_fast_value = {}
    txcoarse_value = {}
    txdqcoarse_value = {}
    txfine_value = {}
    mrl_value = {} 



    #check for the eddr5 scripts available in the path 
    if os.path.exists(mapping_file):

        dcs_coarse_pattern = re.compile(r"trainingResults.DcsCoarseDly\[(\d+)\]")
        dcs_delay_pattern = re.compile(r"trainingResults.DcsFineDly\[(\d+)\]")
        dcs_vref_pattern = re.compile(r"trainingResults.rcd.DcsVref\[(\d+)\]")

        dca_delay_pattern = re.compile(r"trainingResults.DcaFineDly\[(\d+)\]")
        dca_coarse_pattern = re.compile(r"trainingResults.DcaCoarseDly\[(\d+)\]")
        dca_vref_pattern = re.compile(r"trainingResults.rcd.DcaVref\[(\d+)\]")

        wl_coarse_pattern = re.compile(r"trainingResults.pdaTrainResults\[(\d+)\]\[(\d+)\].dramMr7")
        wl_fine_pattern = re.compile(r"trainingResults.pdaTrainResults\[(\d+)\]\[(\d+)\].dramMr3")

        txvref_pattern = re.compile(r"trainingResults..DramVrefDqMr10\[(\d+)\]\[(\d+)\]")

        mrl_pattern = re.compile(r"trainingResults.TrainedMrl")

        df = pd.read_csv(mapping_file)
        dcs_map_value = {}
        dcs_map_coarse = {}
        dcs_map_vref = {}

        dca_map_value = {}
        dca_map_coarse = {}
        dca_map_vref = {}
        
        wl_map_coarse = {}
        wl_map_fine = {}

        tx_map_vref = {}

        mrl_map = {}

        for index, row in df.iterrows():

            dcs_coarse_match = dcs_coarse_pattern.search(row["Variable"])

            if(dcs_coarse_match):

                cs = dcs_coarse_match.group(1)
                addr = row["Address"].upper()
                dcs_key = int(cs)
                dcs_map_coarse[dcs_key] = addr
    
            dcs_delay_match = dcs_delay_pattern.search(row["Variable"])

            if(dcs_delay_match):

                cs = dcs_delay_match.group(1)
                addr = row["Address"].upper()
                dcs_key = int(cs)
                dcs_map_value[dcs_key] = addr
            
            dcs_vref_match = dcs_vref_pattern.search(row["Variable"])
            if(dcs_vref_match):

                cs = dcs_vref_match.group(1)
                addr = row["Address"].upper()
                dcs_key = int(cs)
                dcs_map_vref[dcs_key] = addr


            dca_coarse_match = dca_coarse_pattern.search(row["Variable"])

            if(dca_coarse_match):

                cs = dca_coarse_match.group(1)
                addr = row["Address"].upper()
                dca_key = int(cs)
                dca_map_coarse[dca_key] = addr
    
            dca_delay_match = dca_delay_pattern.search(row["Variable"])

            if(dca_delay_match):

                cs = dca_delay_match.group(1)
                addr = row["Address"].upper()
                dca_key = int(cs)
                dca_map_value[dca_key] = addr
            
            dca_vref_match = dca_vref_pattern.search(row["Variable"])

            if(dca_vref_match):

                cs = dca_vref_match.group(1)
                addr = row["Address"].upper()
                dca_key = int(cs)
                dca_map_vref[dca_key] = addr
        
            wl_coarse_match = wl_coarse_pattern.search(row["Variable"])

            if(wl_coarse_match):

                r,n = wl_coarse_match.groups()
                addr = row["Address"].upper()
                wl_key = int(r),int(n)
                wl_map_coarse[wl_key] = addr

            wl_fine_match = wl_fine_pattern.search(row["Variable"])
            if(wl_fine_match):

                r,n = wl_fine_match.groups()
                addr = row["Address"].upper()
                wl_key = int(r),int(n)
                wl_map_fine[wl_key] = addr

            
            txvref_match = txvref_pattern.search(row["Variable"])
            if(txvref_match):
                r,n = txvref_match.groups()
                addr = row["Address"].upper()
                tx_key = int(r),int(n)
                tx_map_vref[tx_key] = addr


            mrl_match = mrl_pattern.search(row["Variable"])
            if(mrl_match):
                mrl_key = 0
                addr = row["Address"].upper()
                mrl_map[mrl_key] = addr

    
    
    with open (filename,'r') as file:
        previous_line = ""
        previous_2line = ""
        previous_3line = ""
        tx_prev_line = ""
        tx_prev_2line = ""
        for line in file:

            if("CcdMap" in line):
                if("Socket" in line):
                    for char in line:
                        if char.isdigit():
                            socket = int(char)
                
                if("Node" in line):
                    for char in line:
                        if char.isdigit():
                            node = int(char)

            decoded_match = decoded_pattern.search(line)
            
            if(decoded_match):

                ch,phy,addr,val = decoded_match.groups()

                for key, value in dcs_map_value.items():
                    
                    if(value == addr):
                        
                        dcs_key = socket,node,int(phy),int(ch),int(key)
                        if(int(key) == 0):
                            vars = hex(int(val,16) & int('0xFF',16))
                        if(int(key) == 1):
                            vars = hex((int(val,16) & int('0xFF00',16)) >> 8)
                        dcs_value[dcs_key] = int(vars,16)
                
                for key, value in dcs_map_coarse.items():
                    
                    if(value == addr):
                        
                        dcs_key = socket,node,int(phy),int(ch),int(key)
                        if(int(key) == 0):
                            vars = hex((int(val,16) & int('0xFF0000',16)) >> 16)
                        if(int(key) == 1):
                            vars = hex((int(val,16) & int('0xFF000000',16)) >> 24)
                        dcs_coarse[dcs_key] = int(vars,16)

                for key, value in dcs_map_vref.items():
                    
                    if(value == addr):
                        
                        dcs_key = socket,node,int(phy),int(ch),int(key)
                        if(int(key) == 0):
                            vars = hex((int(val,16) & int('0xFF0000',16)) >> 16)
                        if(int(key) == 1):
                            vars = hex((int(val,16) & int('0xFF000000',16)) >> 24)
                        dcs_vref[dcs_key] = int(vars,16)

                for key, value in dca_map_value.items():
                    
                    if(value == addr):
                        
                        dca_key = socket,node,int(phy),int(ch),int(key)
                        if(int(key) == 0 or int(key) == 4):
                            vars = hex(int(val,16) & int('0xFF',16))
                        if(int(key) == 1 or int(key) == 5):
                            vars = hex((int(val,16) & int('0xFF00',16)) >> 8)
                        if(int(key) == 2 or int(key) == 6):
                            vars = hex((int(val,16) & int('0xFF0000',16)) >> 16)
                        if(int(key) == 3 or int(key) == 7):
                            vars = hex((int(val,16) & int('0xFF000000',16)) >> 24)
                        dca_value[dca_key] = int(vars,16)
                
                for key, value in dca_map_coarse.items():
                    
                    if(value == addr):
                        
                        dca_key = socket,node,int(phy),int(ch),int(key)
                        if(int(key) == 0 or int(key) == 4):
                            vars = hex(int(val,16) & int('0xFF',16))
                        if(int(key) == 1 or int(key) == 5):
                            vars = hex((int(val,16) & int('0xFF00',16)) >> 8)
                        if(int(key) == 2 or int(key) == 6):
                            vars = hex((int(val,16) & int('0xFF0000',16)) >> 16)
                        if(int(key) == 3 or int(key) == 7):
                            vars = hex((int(val,16) & int('0xFF000000',16)) >> 24)
                        dca_coarse[dca_key] = int(vars,16)

                for key, value in dca_map_vref.items():
                    
                    if(value == addr):
                        
                        dca_key = socket,node,int(phy),int(ch),int(key)
                        if(int(key) == 0 or int(key) == 4):
                            vars = hex(int(val,16) & int('0xFF',16))
                        if(int(key) == 1 or int(key) == 5):
                            vars = hex((int(val,16) & int('0xFF00',16)) >> 8)
                        if(int(key) == 2 or int(key) == 6):
                            vars = hex((int(val,16) & int('0xFF0000',16)) >> 16)
                        if(int(key) == 3 or int(key) == 7):
                            vars = hex((int(val,16) & int('0xFF000000',16)) >> 24)
                        dca_vref[dca_key] = int(vars,16)

                for key, value in wl_map_coarse.items():
                    if(value == addr):      
                        wl_coarse_key = socket,node,int(phy),int(ch),int(key[0]),int(key[1])
                        wlcoarse_value[wl_coarse_key] = int(val,16)
                
                for key, value in wl_map_fine.items():
                    if(value == addr):      
                        wl_value_key = socket,node,int(phy),int(ch),int(key[0]),int(key[1])
                        wl_value[wl_value_key] = int(val,16)

                for key, value in tx_map_vref.items():
                    if(value == addr):      
                        tx_key = socket,node,int(phy),int(ch),int(key[0]),int(key[1])
                        txvref_value[tx_key] = int(val,16)


                for key, value in mrl_map.items():
                    if(value == addr):      
                        mrl_value_key = socket,node,int(phy),int(ch),int(key)
                        mrl_value[mrl_value_key] = int(val,16) >> 16
            

            # Get RxEN value
            rxen_match = pattern_rxen.search(previous_3line)
            if rxen_match:
                rxen_channel, rxen_subchannel, rxen_rank, rxen_type = (
                    rxen_match.groups()
                )
                if ("BTFW" in previous_2line) and ("Db0Nb0" in previous_2line):
                    replace_line = line.replace("|", " ")
                    decode_item = replace_line.split()
                    
                    if len(decode_item) == 16:
                        if (
                            decode_item[6].strip().isdigit()
                            and decode_item[15].strip().isdigit()
                        ):
                            
                            if rxen_type == "RxEnCoarseDly":
                                for i in range(0, 10):
                                    rxen_key = (
                                        socket,
                                        node,     
                                        int(rxen_subchannel),
                                        int(rxen_channel),
                                        int(rxen_rank),
                                        i,
                                    )
                                    rxencoarsedly_value[rxen_key] = int(
                                        decode_item[i + 6].strip()
                                    )

                                    
                                    
                            elif rxen_type == "RxEnFineDly":
                                for i in range(0, 10):
                                    rxen_key = (
                                        socket,
                                        node,
                                        int(rxen_subchannel),
                                        int(rxen_channel),
                                        int(rxen_rank),
                                        i,
                                    )
                                    rxen_value[rxen_key] = int(
                                        decode_item[i + 6].strip()
                                    )
                                    rxencoarsesel_value[rxen_key] = int(
                                        decode_item[i + 6].strip()
                                    )
                
            
            #Rd Eye
            rd_eye_match = pattrn_rd_eye.search(line)
            if(rd_eye_match):
                rx_channel, rx_subchannel,rx_phase, rx_byte, rx_nibble, rx_dq,rx_centerdelay= (
                    rd_eye_match.groups()
                )
                
                if rx_byte == "0":
                    if rx_nibble == "0":
                        rx_key = (
                            socket,
                            node,
                            int(rx_subchannel),
                            int(rx_channel),
                            0,
                            0,
                            int(rx_dq),
                        )
                    else:
                        rx_key = (
                            socket,
                            node,
                            int(rx_subchannel),
                            int(rx_channel),
                            0,
                            1,
                            int(rx_dq),
                        )
                elif rx_byte == "1":
                    if rx_nibble == "0":
                        rx_key = (
                            socket,
                            node,
                            int(rx_subchannel),
                            int(rx_channel),
                            0,
                            2,
                            int(rx_dq),
                        )
                    else:
                        rx_key = (
                            socket,
                            node,
                            int(rx_subchannel),
                            int(rx_channel),
                            0,
                            3,
                            int(rx_dq),
                        )
                elif rx_byte == "2":
                    if rx_nibble == "0":
                        rx_key = (
                            socket,
                            node,
                            int(rx_subchannel),
                            int(rx_channel),
                            0,
                            4,
                            int(rx_dq),
                        )
                    else:
                        rx_key = (
                            socket,
                            node,
                            int(rx_subchannel),
                            int(rx_channel),
                            0,
                            5,
                            int(rx_dq),
                        )
                elif rx_byte == "3":
                    if rx_nibble == "0":
                        rx_key = (
                            socket,
                            node,
                            int(rx_subchannel),
                            int(rx_channel),
                            0,
                            6,
                            int(rx_dq),
                        )
                    else:
                        rx_key = (
                            socket,
                            node,
                            int(rx_subchannel),
                            int(rx_channel),
                            0,
                            7,
                            int(rx_dq),
                        )
                elif rx_byte == "4":
                    if rx_nibble == "0":
                        rx_key = (
                            socket,
                            node,
                            int(rx_subchannel),
                            int(rx_channel),
                            0,
                            8,
                            int(rx_dq),
                        )
                    else:
                        rx_key = (
                            socket,
                            node,
                            int(rx_subchannel),
                            int(rx_channel),
                            0,
                            9,
                            int(rx_dq),
                        )
                
                if(rx_phase == '0'):
                    rxdlyodd_value[rx_key] =  int(rx_centerdelay,16)
                if(rx_phase == '1'):
                    rxdlyeven_value[rx_key] =  int(rx_centerdelay,16)
            

            txen_match = pattern_txen.search(previous_2line)
            if(txen_match):
                # txen_channel, txen_subchannel, txen_rank, txen_type = (
                #     txen_match.groups()
                # )
                
                if ("WR TRAIN" in previous_line) and ("Db" in previous_line):

                    tx_prev_line = previous_line
                    tx_prev_2line = previous_2line
                    
            
            if("WR TRAIN" not in line):
                tx_prev_2line = ""
                tx_prev_line = "" 


            txen_match = pattern_txen.search(tx_prev_2line)
            if(txen_match):
                txen_channel, txen_subchannel, txen_rank, txen_type = (
                    txen_match.groups()
                )
                
                if ("WR TRAIN" in tx_prev_line) and ("Db" in tx_prev_line):
                    
                    replace_line = line.replace("|", " ")
                    decode_item = replace_line.split()
                    #print(decode_item)
                    if txen_type == "TxDQ Fine Delay":
                        
                        if len(decode_item) == 16:
                            if (
                                decode_item[7].strip().isdigit()
                                and decode_item[15].strip().isdigit()
                            ):
                                for i in range(0, 8):
                                    txen_key = (
                                        socket,
                                        node,
                                        int(txen_subchannel),
                                        int(txen_channel),
                                        int(txen_rank),
                                        int(decode_item[7]),
                                        i,
                                    )
                                    txfine_value[txen_key] = int(
                                        decode_item[i + 8].strip()
                                    )
                    if txen_type == "TxDQ Coarse Delay":
                        
                        if len(decode_item) == 16:
                            if (
                                decode_item[7].strip().isdigit()
                                and decode_item[15].strip().isdigit()
                            ):
                                for i in range(0, 8):
                                    txen_key = (
                                        socket,
                                        node,
                                        int(txen_subchannel),
                                        int(txen_channel),
                                        int(txen_rank),
                                        int(decode_item[7]),
                                        i,
                                    )
                                    txdqcoarse_value[txen_key] = int(
                                        decode_item[i + 8].strip()
                                    )
                    if txen_type == "TxDQ Nibble Coarse":

                        if len(decode_item) == 10:
                            if (
                                decode_item[7].strip().isdigit()
                                and decode_item[9].strip().isdigit()
                            ):
                                for i in range(0, 2):
                                    txen_key = (
                                        socket,
                                        node,
                                        int(txen_subchannel),
                                        int(txen_channel),
                                        int(txen_rank),
                                        int(decode_item[7]),
                                        i,
                                        0
                                    )
                                    txcoarse_value[txen_key] = int(
                                        decode_item[i + 8].strip()
                                    )
                    

            previous_3line = previous_2line      
            previous_2line = previous_line
            previous_line = line

    return (
        dcs_value,
        dcs_coarse,
        dca_value,
        dca_coarse,
        wl_value,
        wlcoarse_value,
        rxen_value,
        rxencoarsedly_value,
        rxencoarsesel_value,
        rxdlyevenu_value,
        rxdlyoddu_value,
        rxdlyevenl_value,
        rxdlyoddl_value,      
        rxvref_value,
        rxvref_fast_value,
        txcoarse_value,
        txdqcoarse_value,
        txfine_value,
        mrl_value,
    )


def detect_DCS_DCA(filename):
    # Regex pattern to capture all relevant values
    ###rcd_pattern = re.compile(r"RCD Write Channel (\d+) SubChannel (\d+) Page (0x[0-9A-Fa-f]+) Register (0x[0-9A-Fa-f]+) Data (0x[0-9A-Fa-f]+)")
    ##CHANNEL: 7,  PHY: 1,  PHYINIT: [MemDdr5RcdWriteWrapper]SubChannel: 1, Dimm: 0 Page: 0x0 RW47 data is 0x13
    rcd_pattern = re.compile(
        r"CHANNEL:\s*([0-9]+),\s*PHY:\s*([0-9]+),\s*PHYINIT:\s*\[MemDdr5RcdWriteWrapper\]SubChannel:\s*([0-9]+),\s*Dimm:\s*([0-9]+)\s*Page:\s*(0x[0-9A-Fa-f]+)\s*RW([0-9A-Fa-f]+)\s*data is\s*(0x[0-9A-Fa-f]+)"
    )
    ##CHANNEL: 0,  PHY: 0,  PHYINIT: BTFW: [DCSDLYSW] min_dly: 54, max_dly: 172, dlyStep: 1 at dcs0
    ##CHANNEL: 0,  PHY: 0,  PHYINIT: BTFW: [DCSTM] vref = 45, winMax = 118, vref_w = 45, dly_g = 113
    dcs_dly_pattern = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DCSDLYSW\]\s*min_dly:\s*(\d+),\s*max_dly:\s*(\d+),\s*dlyStep:\s*(\d+)\s*at\s*dcs(\d+)"
    )
    dcs_vref_pattern = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DCSTM\]\s*vref\s*=\s*(\d+),\s*winMax\s*=\s*(\d+),\s*vref_w\s*=\s*(\d+),\s*dly_g\s*=\s*(\d+)"
    )
    ##CHANNEL: 7,  PHY: 1,  PHYINIT: BTFW: [DCADLYSW]: pin:7 left:266 right:309 window:43 dlystep:1 dly:159
    ##CHANNEL: 7,  PHY: 1,  PHYINIT: BTFW: [DCATM] vref = 19, win = 43,  winMax = 58, vref_w = 58, dly_g = 160
    dca_dly_pattern = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DCADLYSW\]:\s*pin:(\d+)\s*left:(\d+)\s*right:(\d+)\s*window:(\d+)\s*dlystep:(\d+)\s*dly:(\d+)"
    )
    dca_vref_pattern = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[DCATM\]\s*vref\s*=\s*(\d+),\s*win\s*=\s*(\d+),\s*winMax\s*=\s*(\d+),\s*vref_w\s*=\s*(\d+),\s*dly_g\s*=\s*(\d+)"
    )
    # Dictionary to store the latest Data value for each unique (Channel, SubChannel, Page, Register)
    dcs_dly = {}
    dcs_vref = {}
    dcs_win = {}
    dcs_eye = {}
    dca_dly = {}
    dca_vref = {}
    dca_win = {}
    dca_eye = {}
    # Process each line in the log
    with open(filename, "r") as file:
        previous_line = ""
        dimm = 0
        for line in file:
            rcd_match = rcd_pattern.search(line)
            dcsvref_match = dcs_vref_pattern.search(line)
            if dcsvref_match:
                dcsdly_match = dcs_dly_pattern.search(previous_line)
                if dcsdly_match:
                    channel, subchannel, vref, winMax, vrefMax, delayMax = (
                        dcsvref_match.groups()
                    )
                    channel2, subchannel2, left, right, dcs_step, cs_pin = (
                        dcsdly_match.groups()
                    )
                    if channel == channel2 and subchannel == subchannel2:
                        dcs_key = (
                            int(channel),
                            int(subchannel),
                            int(dimm),
                            int(cs_pin),
                        )  # Unique key for each entry
                        dcs_dly[dcs_key] = int(delayMax)  # Store the latest occurrence
                        dcs_vref[dcs_key] = int(vrefMax)
                        if dcs_key not in dcs_eye:
                            dcs_eye[dcs_key] = []
                        dcs_eye[dcs_key].append([int(vref), int(left)])
                        dcs_eye[dcs_key].append([int(vref), int(right)])
                        dcs_win[dcs_key] = int(winMax)
            dcavref_match = dca_vref_pattern.search(line)
            if dcavref_match:
                dcadly_match = dca_dly_pattern.search(previous_line)
                if dcadly_match:
                    channel, subchannel, ca_pin, left, right, window, step, delay = (
                        dcadly_match.groups()
                    )
                    channel2, subchannel2, vref, window2, winMax, vrefMax, delayMax = (
                        dcavref_match.groups()
                    )
                    if channel == channel2 and subchannel == subchannel2:
                        dcadly_key = (
                            int(channel),
                            int(subchannel),
                            int(ca_pin),
                        )  # Unique key for each entry
                        dca_dly[dcadly_key] = int(
                            delayMax
                        )  # Store the latest occurrence
                        dcavref_key = (
                            int(channel),
                            int(subchannel),
                            int(dimm),
                            int(ca_pin),
                        )
                        dca_vref[dcavref_key] = int(vrefMax)
                        dcaeye_key = (
                            int(channel),
                            int(subchannel),
                            int(dimm),
                            int(ca_pin),
                        )
                        if dcaeye_key not in dca_eye:
                            dca_eye[dcaeye_key] = []
                        dca_eye[dcaeye_key].append([int(vref), int(left)])
                        dca_eye[dcaeye_key].append([int(vref), int(right)])
                        dca_win[dcavref_key] = int(winMax)
            else:
                if rcd_match:
                    (rcd_channel, rcd_subchannel, sub, dimm, page, register, value) = (
                        rcd_match.groups()
                    )
            previous_line = line
    return dcs_dly, dcs_vref, dcs_win, dcs_eye, dca_dly, dca_vref, dca_win, dca_eye


def detect_wl_rxen_rxtx(filename):
    pattern_wl = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),.*<< Rank:\s*(\d+),\s*(\w+)\s*(\w+)"
    )
    pattern_rxen = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),.*<< Rank:\s*(\d+),\s*(\w+)"
    )
    pattern_rx1 = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*Dumping\s*Rd\s*Eyes.*Cs:\s*(\d+),\s*Dbyte:\s*(\d+),\s*Nibble:\s*(\d+),\s*Dq:\s*(\d+)"
    )
    pattern_rx2 = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:.*<<---\s*DelayOffset:\s*(\d+),\s*CenterDelay:\s*(\d+),\s*CenterVref:\s*(\d+)\s*--->"
    )
    pattern_txrank = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*BTFW:\s*\[WR\s*TRAIN\]\s*WrVrefDelayTraining\s*\-\s*Delay\s*training\s*start\s*rank\s*(\d+)"
    )
    pattern_tx1 = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:\s*Dumping\s*Wr\s*Eye.*Ch:\s*(\d+),\s*Db:\s*(\d+),\s*Dq:\s*(\d+)"
    )
    pattern_tx2 = re.compile(
        r"CHANNEL:\s*(\d+),\s*PHY:\s*(\d+),\s*PHYINIT:.*<<---\s*DelayOffset:\s*(\d+),\s*CenterDelay:\s*(\d+),\s*CenterVref:\s*(\d+)\s*--->"
    )
    wl_value = {}
    rxen_value = {}
    rxdly_value = {}
    rxvref_value = {}
    txdly_value = {}
    txvref_value = {}
    txrank = 0
    # Process each line in the log
    with open(filename, "r") as file:
        previous_line = ""
        previous_2line = ""
        #dimm = 0
        for line in file:
            # Get WL value
            wl_match = pattern_wl.search(previous_2line)
            if wl_match:
                wl_channel, wl_subchannel, wl_rank, wl_type, wl_type2 = (
                    wl_match.groups()
                )
                if ("WL TRAIN" in previous_line) and ("Nb0" in previous_line):
                    decode_item = line.split("|")
                    if len(decode_item) == 12:
                        if (
                            decode_item[1].strip().isdigit()
                            and decode_item[10].strip().isdigit()
                        ):
                            if wl_type == "TxDQS" and wl_type2 == "Coarse":
                                for i in range(0, 10):
                                    wl_key = (
                                        int(wl_channel),
                                        int(wl_subchannel),
                                        int(wl_rank),
                                        0,
                                        i,
                                    )
                                    wl_value[wl_key] = int(decode_item[i + 1].strip())
                            elif wl_type == "TxDQS" and wl_type2 == "Fine":
                                for i in range(0, 10):
                                    wl_key = (
                                        int(wl_channel),
                                        int(wl_subchannel),
                                        int(wl_rank),
                                        1,
                                        i,
                                    )
                                    wl_value[wl_key] = int(decode_item[i + 1].strip())
                            elif wl_type == "MR3":
                                for i in range(0, 10):
                                    wl_key = (
                                        int(wl_channel),
                                        int(wl_subchannel),
                                        int(wl_rank),
                                        2,
                                        i,
                                    )
                                    wl_value[wl_key] = int(decode_item[i + 1].strip())
                            elif wl_type == "MR7":
                                for i in range(0, 10):
                                    wl_key = (
                                        int(wl_channel),
                                        int(wl_subchannel),
                                        int(wl_rank),
                                        3,
                                        i,
                                    )
                                    wl_value[wl_key] = int(decode_item[i + 1].strip())
            # Get RxEN value
            rxen_match = pattern_rxen.search(previous_2line)
            if rxen_match:
                rxen_channel, rxen_subchannel, rxen_rank, rxen_type = (
                    rxen_match.groups()
                )
                if ("BTFW" in previous_line) and ("Db0Nb0" in previous_line):
                    replace_line = line.replace("|", " ")
                    decode_item = replace_line.split()
                    if len(decode_item) == 16:
                        if (
                            decode_item[6].strip().isdigit()
                            and decode_item[15].strip().isdigit()
                        ):
                            if rxen_type == "RxEnCoarseDly":
                                for i in range(0, 10):
                                    rxen_key = (
                                        int(rxen_channel),
                                        int(rxen_subchannel),
                                        int(rxen_rank),
                                        0,
                                        i,
                                    )
                                    rxen_value[rxen_key] = int(
                                        decode_item[i + 6].strip()
                                    )
                            elif rxen_type == "RxEnFineDly":
                                for i in range(0, 10):
                                    rxen_key = (
                                        int(rxen_channel),
                                        int(rxen_subchannel),
                                        int(rxen_rank),
                                        1,
                                        i,
                                    )
                                    rxen_value[rxen_key] = int(
                                        decode_item[i + 6].strip()
                                    )
            # Get Rx Train Value
            rx_match1 = pattern_rx1.search(previous_line)
            if rx_match1:
                rx_channel, rx_subchannel, rx_rank, rx_byte, rx_nibble, rx_dq = (
                    rx_match1.groups()
                )
                rx_match2 = pattern_rx2.search(line)
                if rx_match2:
                    (
                        rx_channel2,
                        rx_subchannel2,
                        rx_delayoffset,
                        rx_centerdelay,
                        rx_vref,
                    ) = rx_match2.groups()
                    if rx_channel == rx_channel2 and rx_subchannel == rx_subchannel2:
                        if rx_byte == "0":
                            if rx_nibble == "0":
                                rx_key = (
                                    int(rx_channel),
                                    int(rx_subchannel),
                                    int(rx_rank),
                                    0,
                                    int(rx_dq),
                                )
                            else:
                                rx_key = (
                                    int(rx_channel),
                                    int(rx_subchannel),
                                    int(rx_rank),
                                    1,
                                    int(rx_dq),
                                )
                        elif rx_byte == "1":
                            if rx_nibble == "0":
                                rx_key = (
                                    int(rx_channel),
                                    int(rx_subchannel),
                                    int(rx_rank),
                                    2,
                                    int(rx_dq),
                                )
                            else:
                                rx_key = (
                                    int(rx_channel),
                                    int(rx_subchannel),
                                    int(rx_rank),
                                    3,
                                    int(rx_dq),
                                )
                        elif rx_byte == "2":
                            if rx_nibble == "0":
                                rx_key = (
                                    int(rx_channel),
                                    int(rx_subchannel),
                                    int(rx_rank),
                                    4,
                                    int(rx_dq),
                                )
                            else:
                                rx_key = (
                                    int(rx_channel),
                                    int(rx_subchannel),
                                    int(rx_rank),
                                    5,
                                    int(rx_dq),
                                )
                        elif rx_byte == "3":
                            if rx_nibble == "0":
                                rx_key = (
                                    int(rx_channel),
                                    int(rx_subchannel),
                                    int(rx_rank),
                                    6,
                                    int(rx_dq),
                                )
                            else:
                                rx_key = (
                                    int(rx_channel),
                                    int(rx_subchannel),
                                    int(rx_rank),
                                    7,
                                    int(rx_dq),
                                )
                        elif rx_byte == "4":
                            if rx_nibble == "0":
                                rx_key = (
                                    int(rx_channel),
                                    int(rx_subchannel),
                                    int(rx_rank),
                                    8,
                                    int(rx_dq),
                                )
                            else:
                                rx_key = (
                                    int(rx_channel),
                                    int(rx_subchannel),
                                    int(rx_rank),
                                    9,
                                    int(rx_dq),
                                )
                        rxdly_value[rx_key] = int(rx_delayoffset) + int(rx_centerdelay)
                        rxvref_value[rx_key] = int(rx_vref)
            # Get Tx Train Value
            txrank_match = pattern_txrank.search(line)
            if txrank_match:
                txrank_ch, txrank_sub, txrank = txrank_match.groups()
            tx_match1 = pattern_tx1.search(previous_line)
            if tx_match1:
                ##missing rank info in Wr Eye is Ch suppose to be Rank?
                tx_channel, tx_subchannel, tx_ch, tx_byte, tx_dq = tx_match1.groups()
                tx_match2 = pattern_tx2.search(line)
                if tx_match2:
                    (
                        tx_channel2,
                        tx_subchannel2,
                        tx_delayoffset,
                        tx_centerdelay,
                        tx_vref,
                    ) = tx_match2.groups()
                    if tx_channel == tx_channel2 and tx_subchannel == tx_subchannel2:
                        tx_key = (
                            int(tx_channel),
                            int(tx_subchannel),
                            int(txrank),
                            tx_byte,
                            int(tx_dq),
                        )
                        txdly_value[tx_key] = int(tx_delayoffset) + int(tx_centerdelay)
                        txvref_value[tx_key] = int(tx_vref)
            previous_2line = previous_line
            previous_line = line
    return wl_value, rxen_value, rxdly_value, rxvref_value, txdly_value, txvref_value


def process_data(data):
    result = []
    for key, value in data.items():
        channel, subchannel, rank, pin = key
        entry = {
            "channel": channel,
            "subchannel(phy)": subchannel,
            "rank": rank,
            "pin": pin,
            "trained_value": value,
        }
        result.append(entry)
    return result


def process_data_no_dimm(data):
    result = []
    for key, value in data.items():
        soc, iod, channel, subchannel, pin = key
        entry = {
            "Socket": soc,
            "IOD": iod,  
            "channel": channel,
            "subchannel(phy)": subchannel,
            "pin": pin,
            "trained_value": value,
        }
        result.append(entry)
    return result


def process_data_wl(data):
    result = []
    for key, value in data.items():
        soc, iod, channel, subchannel, rank, nibble = key
        entry = {
            "Socket": soc,
            "IOD": iod,         
            "channel": channel,
            "subchannel(phy)": subchannel,
            "rank": rank,
            "nibble": nibble,
            "trained_value": value,
        }
        result.append(entry)
    return result


def process_data_rxen(data):
    result = []
    for key, value in data.items():
        soc, iod, channel, subchannel, rank, param, nibble = key
        if param == 0:
            entry = {
                "Param": "Coarse RxEN",
                "Socket": soc,
                "IOD": iod,                 
                "channel": channel,
                "subchannel(phy)": subchannel,
                "rank": rank,
                "nibble": nibble,
                "trained_value": value,
            }
        elif param == 1:
            entry = {
                "Param": "Fine RxEN",
                "Socket": soc,
                "IOD": iod,                  
                "channel": channel,
                "subchannel(phy)": subchannel,
                "rank": rank,
                "nibble": nibble,
                "trained_value": value,
            }
        result.append(entry)
    return result


def process_data_2d(data):
    result = []
    for key, value in data.items():
        soc, iod, channel, subchannel, rank, nibble, pin = key
        entry = {
            "Socket": soc,
            "IOD": iod,         
            "channel": channel,
            "subchannel(phy)": subchannel,
            "rank": rank,
            "nibble": nibble,
            "pin": pin,
            "trained_value": value,
        }
        result.append(entry)
    return result


def process_data_mrl(data):
    result = []
    for key, value in data.items():
        soc, iod, channel, subchannel, nibble = key
        entry = {
            "Socket": soc,
            "IOD": iod,           
            "channel": channel,
            "subchannel(phy)": subchannel,
            "rank": "NA",
            "nibble": nibble,
            "pin": "NA",
            "trained_value": value,
        }
        result.append(entry)
    return result


def process_data_rxvref(data):
    result = []
    for key, value in data.items():
        soc, iod, channel, subchannel, nibble, pin = key
        entry = {
            "Socket": soc,
            "IOD": iod,           
            "channel": channel,
            "subchannel(phy)": subchannel,
            "rank": "NA",
            "nibble": nibble,
            "pin": pin,
            "trained_value": value,
        }
        result.append(entry)
    return result


def process_data_txcoarse(data):
    result = []
    for key, value in data.items():
        soc, iod, channel, subchannel, rank, param, nibble = key
        entry = {
            "Param": "Tx2D Coarse",
            "Socket": soc,
            "IOD": iod,   
            "channel": channel,
            "subchannel(phy)": subchannel,
            "rank": rank,
            "nibble": nibble,
            "trained_value": value,
        }
        result.append(entry)
    return result


def calculation(
    dcs_value,
    dcs_coarse,
    dca_value,
    dca_coarse,
    wl_value,
    wlcoarse_value,
    rxen_value,
    rxencoarsedly_value,
    rxencoarsesel_value,
    rxdlyevenu_value,
    rxdlyoddu_value,
    rxdlyevenl_value,
    rxdlyoddl_value,      
    rxvref_value,
    rxvref_fast_value,
    txcoarse_value,
    txdqcoarse_value,
    txfine_value
):
    # DCS
    dcs_result = {}
    for key, value in dcs_coarse.items():
        soc, iod, ch, sub, cs = key
        ##TxCsCoarseDly * 64 + stdqs_mdqs_dqsuTx[tc]_TxClkGenPiCode
        dcs_result[key] = (value * 64) + dcs_value[key]
    # DCA
    dca_result = {}
    for key, value in dca_coarse.items():
        soc, iod, ch, sub, ca = key
        ##TxCaCoarseDly * 64 + stdqs_mdqs_dqtx[ul][0-3]_TxClkGenPiCode
        dca_result[key] = (value * 64) + dca_value[key]
    # WL
    wl_result = {}
    for key, value in wlcoarse_value.items():
        soc, iod, ch, sub, r, db = key
        ##DqsCoarseDly * 64 + stdqs_mdqs_dqs[ul]Txt_TxClkGenPiCode
        wl_result[key] = (value * 64) + wl_value[key]
    # RxEN
    rxen_result = {}
    for key, value in rxencoarsedly_value.items():
        soc, iod, ch, sub, r, db = key
        ##int(row['RxDqsCoarseDlyTg DqsCoarseDly'])*128 + np.floor((int(row[f'RXDQS_{ul.upper()}_RDGATE_DL_CTRL srdqs_mdqs_dqs{ul}_RdGateDlCoarseSel'])*16 + int(row[f'RXDQS_{ul.upper()}_RDGATE_DL_CTRL srdqs_mdqs_dqs{ul}_RdGateDlPiCode']))/4)
        rxen_result[key] = (value * 128) + np.floor(((rxencoarsesel_value[key]*16)+rxen_value[key])/4)
    #Read Eye 
    #rx2d even Ucode    
    rxdlyevenu_result = {}
    for key, value in rxdlyevenu_value.items():
        soc, iod, ch, sub, r, db, dq = key
        if value >= 64:
            rxdlyevenu_result[key]= 128-value
        else:
            rxdlyevenu_result[key]= value
    #rx2d odd Ucode
    rxdlyoddu_result = {}
    for key, value in rxdlyoddu_value.items():
        soc, iod, ch, sub, r, db, dq = key
        if value >= 64:
            rxdlyoddu_result[key]= 128-value
        else:
            rxdlyoddu_result[key]= value
    #rx2d even Lcode    
    rxdlyevenl_result = {}
    for key, value in rxdlyevenl_value.items():
        soc, iod, ch, sub, r, db, dq = key
        if value >= 64:
            rxdlyevenl_result[key]= 128-value
        else:
            rxdlyevenl_result[key]= value
    #rx2d odd Lcode
    rxdlyoddl_result = {}
    for key, value in rxdlyoddl_value.items():
        soc, iod, ch, sub, r, db, dq = key
        if value >= 64:
            rxdlyoddl_result[key]= 128-value
        else:
            rxdlyoddl_result[key]= value    

    # Tx2d
    # db0n0       db0n1       db1n0       db1n1       db2n0       db2n1       db3n0       db3n1       db4n0       db4n1
    # db0bit0-3   db0bit4-7   db1bit0-3   db1bit4-7   db2bit0-3   db2bit4-7   db3bit0-3   db3bit4-7   db4bit0-3   db4bit4-7
    # nibble0     nibble1     nibble2     nibble3     nibble4     nibble5     nibble6     nibble7     nibble8     nibble9
    tx2d_result = {}
    for key, value in txcoarse_value.items():
        soc, iod, ch, sub, r, db, n, dq = key
        dqcoarse_key = (soc, iod, ch, sub, r, db, n)
        new_dq = (n * 4) + dq
        fine_key = (soc, iod, ch, sub, r, db, new_dq)
        nibble = (db * 2) + n
        tx2d_key = (soc, iod, ch, sub, r, nibble, dq)
        ##(DqCoarseDly + CoarseDly) * 64 + stdqs_mdqs_dqtx[ul][0-3]_TxClkGenPiCode
        tx2d_result[tx2d_key] = (
            value + txdqcoarse_value[dqcoarse_key]
        ) * 64 + txfine_value[fine_key]

    

    return (
        dcs_result, 
        dca_result, 
        wl_result, 
        rxen_result, 
        tx2d_result, 
        rxdlyevenu_result,
        rxdlyoddu_result,
        rxdlyevenl_result,
        rxdlyoddl_result
    )        

def calculate_standard_deviation_and_range(analysis_csv):
    # Step 1: Read the CSV data
    df_analysis = pd.read_csv(analysis_csv)
    # Ensure that the 'trained_value' column is included in the columns of interest

    # Step 2: Identify the columns related to 'trained_value' and runX (dynamically find columns that start with 'run')
    columns_of_interest = ["trained_value"] + [col for col in df_analysis.columns if col.startswith("run")]

    # Step 3: Iterate through each row and calculate the standard deviation and range
    df_analysis["standard_deviation"] = df_analysis[columns_of_interest].std(axis=1, ddof=0)
    df_analysis["range"] = df_analysis[columns_of_interest].max(axis=1) - df_analysis[columns_of_interest].min(axis=1)

    # Step 4 Add pass/fail if range >7
    df_analysis["Pass_Fail"] = df_analysis["range"].apply(lambda x: "Fail" if x > 7 else "Pass")

    # Step 5 Check if 'Param' is 'MRL' and 'trained_value' is not between 14 and 17 for all run columns
    df_analysis["Pass_Fail"] = df_analysis.apply(
        lambda row: "Fail" if (row["Param"] == "MRL" and not (14 <= row["trained_value"] <= 17)) else row["Pass_Fail"],
        axis=1,
    )
    run_columns = [col for col in df_analysis.columns if col.startswith("run")]
    df_analysis["Pass_Fail"] = df_analysis.apply(
        lambda row: "Fail" if (row["Param"] == "MRL" and not all(14 <= row[col] <= 17 for col in run_columns)) else row["Pass_Fail"],
        axis=1,
    )

    # Step 6: Copy 'byte' value to new column 'nibble' for 'WL' or 'RXEN' params
    #df_analysis["nibble"] = df_analysis.apply(
    #    lambda row: row["nibble"] if row["Param"] in ["WL", "RXEN"] else "", axis=1
    #)
    # Step 7: Write the updated DataFrame back to the CSV
    df_analysis.to_csv(analysis_csv, index=False)

    # Step 8 Print out/return failures/all pass
    failures = df_analysis[df_analysis["Pass_Fail"] == "Fail"]

    # Step 9: Create a new DataFrame with the max of each range column for each param
    max_range_per_param = df_analysis.groupby("Param")["range"].max().reset_index()
    max_range_per_param.columns = ["Param", "Max Range"]

    # Print the new DataFrame
    print("Max range for each param:")
    print(max_range_per_param)
    if not failures.empty:
        print("Failing rows:")
        print(failures)
        return failures
    else:
        print("All Pass")
        return None


def process_csrdump(
    filename, outputfile, run, inputbase, inputhost, inputbios, analysis_csv
):
    # dcs_dly, dcs_vref, dcs_win, dcs_eye, dca_dly, dca_vref, dca_win, dca_eye  = detect_DCS_DCA(filename)
    (
        dcs_value,
        dcs_coarse,
        dca_value,
        dca_coarse,
        wl_value,
        wlcoarse_value,
        rxen_value,
        rxencoarsedly_value,
        rxencoarsesel_value,
        rxdlyevenu_value,
        rxdlyoddu_value,
        rxdlyevenl_value,
        rxdlyoddl_value,      
        rxvref_value,
        rxvref_fast_value,
        txcoarse_value,
        txdqcoarse_value,
        txfine_value,
        mrl_value,
    ) = detect_decoded_log(filename)
    (
        dcs_result, 
        dca_result, 
        wl_result, 
        rxen_result, 
        tx2d_result, 
        rxdlyevenu_result,
        rxdlyoddu_result,
        rxdlyevenl_result,
        rxdlyoddl_result
    ) = calculation(
        dcs_value,
        dcs_coarse,
        dca_value,
        dca_coarse,
        wl_value,
        wlcoarse_value,
        rxen_value,
        rxencoarsedly_value,
        rxencoarsesel_value,
        rxdlyevenu_value,
        rxdlyoddu_value,
        rxdlyevenl_value,
        rxdlyoddl_value,      
        rxvref_value,
        rxvref_fast_value,
        txcoarse_value,
        txdqcoarse_value,
        txfine_value
    )

    # df_dcs_delay = process_data(dcs_dly)
    # df_dcs_delay = pd.DataFrame(df_dcs_delay)
    # df_dcs_delay['Param'] = "DCS_Delay"
    # df_dcs_delay['byte'] = "NA"

    # df_dcs_vref = process_data(dcs_vref)
    # df_dcs_vref = pd.DataFrame(df_dcs_vref)
    # df_dcs_vref['Param'] = "DCS_vref"
    # df_dca_vref["nibble"] = "NA"

    # df_dca_delay = process_data2(dca_dly)
    # df_dca_delay = pd.DataFrame(df_dca_delay)
    # df_dca_delay['Param'] = "DCA_Delay"
    # df_dca_delay["rank"] = "NA"
    # df_dca_delay["nibble"] = "NA"

    # df_dca_vref = process_data(dca_vref)
    # df_dca_vref = pd.DataFrame(df_dca_vref)
    # df_dca_vref['Param'] = "DCA_vref"
    # df_dca_vref["nibble"] = "NA"

    df_dcs = process_data_no_dimm(dcs_result)
    df_dcs = pd.DataFrame(df_dcs)
    df_dcs["Param"] = "DCS_Delay"
    df_dcs["nibble"] = "NA"
    df_dcs["rank"] = "NA"

    df_dca = process_data_no_dimm(dca_result)
    df_dca = pd.DataFrame(df_dca)
    df_dca["Param"] = "DCA_Delay"
    df_dca["nibble"] = "NA"
    df_dca["rank"] = "NA"

    df_wl = process_data_wl(wl_result)
    df_wl = pd.DataFrame(df_wl)
    df_wl["Param"] = "WL"
    df_wl["pin"] = "NA"

    df_rxen = process_data_wl(rxen_result)
    df_rxen = pd.DataFrame(df_rxen)
    df_rxen["Param"] = "RXEN"
    df_rxen["pin"] = "NA"

    df_rxdlyevenu = process_data_2d(rxdlyevenu_result)
    df_rxdlyevenu = pd.DataFrame(df_rxdlyevenu)
    df_rxdlyevenu["Param"] = "Read eye even U"

    df_rxdlyoddu = process_data_2d(rxdlyoddu_result)
    df_rxdlyoddu = pd.DataFrame(df_rxdlyoddu)
    df_rxdlyoddu["Param"] = "Read eye odd U"

    df_rxdlyevenl = process_data_2d(rxdlyevenl_result)
    df_rxdlyevenl = pd.DataFrame(df_rxdlyevenl)
    df_rxdlyevenl["Param"] = "Read eye even U"

    df_rxdlyoddl = process_data_2d(rxdlyoddl_result)
    df_rxdlyoddl = pd.DataFrame(df_rxdlyoddl)
    df_rxdlyoddl["Param"] = "Read eye odd U"

    df_rxvref = process_data_rxvref(rxvref_value)
    df_rxvref = pd.DataFrame(df_rxvref)
    df_rxvref["Param"] = "Read eye SlowVref"

    df_rxvreffast = process_data_2d(rxvref_fast_value)
    df_rxvreffast = pd.DataFrame(df_rxvreffast)
    df_rxvreffast["Param"] = "Read eye FastVref"

    df_txfdly = process_data_2d(tx2d_result)
    df_txfdly = pd.DataFrame(df_txfdly)
    df_txfdly["Param"] = "Write Eye"

    df_mrl = process_data_mrl(mrl_value)
    df_mrl = pd.DataFrame(df_mrl)
    df_mrl["Param"] = "MRL"

    df = pd.concat(
        [
            df_dcs,
            df_dca,
            df_wl,
            df_rxen,
            df_rxdlyevenu,
            df_rxdlyoddu,
            df_rxdlyevenl,
            df_rxdlyoddl,
            df_rxvref,
            df_rxvreffast,
            df_txfdly,
            df_mrl
        ]
    ).reset_index(drop=True)
    hstnme = [inputhost]
    bios = [inputbios]
    df["Hostname"] = hstnme * len(df)
    df["BIOS"] = bios * len(df)
    df["Filename"] = inputbase
    df["run"] = run

    ordered_columns = [
        "Filename",
        "Hostname",
        "BIOS",
        "Param",
        "Socket",
        "IOD",           
        "channel",
        "subchannel(phy)",
        "rank",
        "nibble",
        "pin",
        "trained_value",
        "run",
    ]
    df = df[ordered_columns]

    df.to_csv(outputfile, mode="a", header=False, index=False)

    if analysis_csv:
        df_analysis = pd.concat(
            [
                df_dcs,
                df_dca,
                df_wl,
                df_rxen,
                df_rxdlyevenu,
                df_rxdlyoddu,
                df_rxdlyevenl,
                df_rxdlyoddl,
                df_rxvref,
                df_rxvreffast,
                df_txfdly,
                df_mrl
            ]
        ).reset_index(drop=True)
        df_analysis["Hostname"] = hstnme * len(df)
        df_analysis["BIOS"] = bios * len(df)
        df_analysis["Filename"] = inputbase
        ordered_columns_analysis = [
            "Filename",
            "Hostname",
            "BIOS",
            "Param",
            "Socket",
            "IOD",  
            "channel",
            "subchannel(phy)",
            "rank",
            "nibble",
            "pin",
            "trained_value",
        ]
        df_analysis = df_analysis[ordered_columns_analysis]

        if run == 0:
            df_analysis.to_csv(analysis_csv, mode="a", header=False, index=False)
        else:
            df_analysis = pd.read_csv(analysis_csv)
            trained_value_column = df["trained_value"]
            run_column_name = f"run{run}"
            df_analysis[run_column_name] = trained_value_column
            df_analysis.to_csv(analysis_csv, mode="w", header=True, index=False)

def trained_csr_csv(inputcsv, jmp_output, analysis_output):
    header_data = {
        "Filename": [],
        "Hostname": [],
        "BIOS": [],
        "Param": [],
        "Socket": [],
        "IOD": [],
        "channel": [],
        "subchannel(phy)": [],
        "rank": [],
        "nibble": [],
        "pin": [],
        "trained_value": [],
        "run": [],
    }
    df = pd.DataFrame(header_data)
    header_newdata = {
        "Filename": [],
        "Hostname": [],
        "BIOS": [],
        "Param": [],
        "Socket": [],
        "IOD": [],        
        "channel": [],
        "subchannel(phy)": [],
        "rank": [],
        "nibble": [],
        "pin": [],
        "trained_value": [],
    }
    df_new = pd.DataFrame(header_newdata)
    run = 0
    hostname = ""
    bios = ""
    if len(inputcsv) >1:
        df.to_csv(jmp_output, mode="w", header=True, index=False)
        df_new.to_csv(analysis_output, mode="w", header=True, index=False)
        for file in inputcsv:
            base = os.path.splitext(os.path.basename(file))[0]
            bios, hostname = get_bios_hostname(base)
            try:
                process_csrdump(file, jmp_output, run, base, hostname, bios, analysis_output)
            except:
                print("CSR: Fail to process file: ",file) 
            run = run + 1
        calculate_standard_deviation_and_range(analysis_output)
    else:
        base = os.path.splitext(os.path.basename(inputcsv[0]))[0]
        df.to_csv(jmp_output, mode="w", header=True, index=False)
        bios, hostname = get_bios_hostname(base)
        process_csrdump(args.log, jmp_output, run, base, hostname, bios, "")
    print("csv file generated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DCA/DCS Training value Processing")
    parser.add_argument("log", help="log file to process", default=None)
    args = parser.parse_args()

    header_data = {
        "Filename": [],
        "Hostname": [],
        "BIOS": [],
        "Param": [],
        "Socket": [],
        "IOD": [],
        "channel": [],
        "subchannel(phy)": [],
        "rank": [],
        "nibble": [],
        "pin": [],
        "trained_value": [],
        "run": [],
    }
    df = pd.DataFrame(header_data)
    header_newdata = {
        "Filename": [],
        "Hostname": [],
        "BIOS": [],
        "Param": [],
        "Socket": [],
        "IOD": [],        
        "channel": [],
        "subchannel(phy)": [],
        "rank": [],
        "nibble": [],
        "pin": [],
        "trained_value": [],
    }
    df_new = pd.DataFrame(header_newdata)
    run = 0
    hostname = ""
    bios = ""
    if os.path.isdir(args.log):
        log_files = get_files_from_directory(args.log)
        newdir, ext = os.path.splitext(os.path.abspath(log_files[0]))
        base = os.path.splitext(os.path.basename(log_files[0]))[0]
        if not os.path.exists(newdir):
            os.mkdir(newdir)
        out_csv = os.path.join(newdir, f"{base}__log_consolidated_jmp.csv")
        df.to_csv(out_csv, mode="w", header=True, index=False)
        analysis_csv = os.path.join(newdir, f"{base}_log_analysis.csv")
        df_new.to_csv(analysis_csv, mode="w", header=True, index=False)
        for file in log_files:
            base = os.path.splitext(os.path.basename(file))[0]
            bios, hostname = get_bios_hostname(base)
            process_csrdump(file, out_csv, run, base, hostname, bios, analysis_csv)
            run = run + 1
        calculate_standard_deviation_and_range(analysis_csv)
    else:
        if os.path.exists(args.log):
            newdir, ext = os.path.splitext(os.path.abspath(args.log))
            base = os.path.splitext(os.path.basename(args.log))[0]
            if not os.path.exists(newdir):
                os.mkdir(newdir)
            out_csv = os.path.join(newdir, f"{base}_log_consolidated_jmp.csv")
            df.to_csv(out_csv, mode="w", header=True, index=False)
            bios, hostname = get_bios_hostname(base)
            process_csrdump(args.log, out_csv, run, base, hostname, bios, "")
        else:
            sys.exit(f"File {args.log} does not exist")
    print("csv file generated")


