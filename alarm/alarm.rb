#!/usr/bin/env ruby

#ALARM Security Engine
#tool to detect scans on network, leaked passwords and credit cards, and XSS attacks
#Written by Victor Ansart

require 'packetfu'
include PacketFu

puts "Starting ALARM security engine..."

$alertNum=1


#looks at TCP flags for FIN, XMASS, and NULL scans
def TCP_Scans(pkt)
	#FIN SCAN DETECTION
	if(pkt.tcp_flags.fin == 1 and pkt.tcp_flags.ack == 0 and pkt.tcp_flags.urg == 0 and pkt.tcp_flags.psh == 0)
		puts $alertNum.to_s() + ". ALERT: FIN SCAN" + " is detected from " + pkt.ip_saddr + " (" + pkt.proto.last + ")!"  
		$alertNum += 1
	end

	#XMASS SCAN DETECTION
	if(pkt.tcp_flags.urg == 1 and pkt.tcp_flags.psh == 1 and pkt.tcp_flags.fin == 1)
		puts $alertNum.to_s() + ". ALERT: XMASS SCAN" + " is detected from " + pkt.ip_saddr + " (" + pkt.proto.last + ")!"  
		$alertNum += 1
	end

	#NULL SCAN DETECTION
	if(pkt.tcp_flags.urg == 0 and pkt.tcp_flags.ack == 0 and pkt.tcp_flags.psh == 0 and pkt.tcp_flags.rst == 0 and pkt.tcp_flags.syn == 0 and pkt.tcp_flags.fin == 0)
		puts $alertNum.to_s() + ". ALERT: NULL SCAN" + " is detected from " + pkt.ip_saddr + " (" + pkt.proto.last + ")!"  
		$alertNum += 1
	end
end


#searches at packet transformed to a string identifying an nmap scan
def NMAP_Scan(pkt)
	if( (pkt.tcp_header.body =~/(N|n)(M|m)(A|a)(P|p)/) != nil )
		puts $alertNum.to_s() + ". ALERT: " + "NMAP scan is detected from " + pkt.ip_saddr + " (" + pkt.proto.last + ")!"  
		$alertNum += 1
		puts pkt.to_s()
	end
end


#searches at packet transformed to a string for credit card patterns
def creditCard(data, pkt)
	cardType = ""
	if( (data =~ /\W4\d{3}(\s|-)?\d{4}(\s|-)?\d{4}(\s|-)?\d{4}\W/ ) != nil )
		cardType = "VISA"
	
	elsif( (data =~ /\W5\d{3}(\s|-)?\d{4}(\s|-)?\d{4}(\s|-)?\d{4}\W/ ) != nil )
		cardType = "MasterCard"
	
	elsif( (data =~ /\W6011(\s|-)?\d{4}(\s|-)?\d{4}(\s|-)?\d{4}\W/ ) != nil )
		cardType = "Discover"
	
	elsif( (data =~ /\W3\d{3}(\s|-)?\d{6}(\s|-)?\d{5}\W/ ) != nil )
		cardType = "American Express"
	end	

	if(cardType != "")
		puts $alertNum.to_s() + ". ALERT: " + cardType + " Credit Card leaked in the clear from " + pkt.ip_saddr + " (" + pkt.proto.last + ")!"  
		$alertNum += 1
	end
end


#searches at packet transformed to a string for password patterns
def passwords(data, pkt)
	if( (data =~ /(\s|_)(p|P)(a|A)(s|S)(s|S)(w|W)(o|O)(r|R)(d|D)(\s|:|=)/) != nil )
		puts $alertNum.to_s() + ". ALERT: " + "password leaked in the clear from " + pkt.ip_saddr + " (" + pkt.proto.last + ")!"  
		$alertNum += 1
	end

end


#searches at packet transformed to a string for XSS
def XSS_Scan(data, pkt)
	if (pkt.tcp_dst == 80)	#look only at http (port 80)
		if( (data =~ /(GET|POST)/) != nil )		#look only in GET or POSTe requests
			if( (data =~ /(<|%3C)(s|S)(c|C)(r|R)(i|I)(p|P)(t|T)(>|%3E)/) != nil)
				puts $alertNum.to_s() + ". ALERT: " + "XSS is detected from " + pkt.ip_saddr + " (" + pkt.proto.last + ")!"  
				$alertNum += 1
			end
		end
	end

end


#function to start sniffing and run scans
def startAlarm(iface)
	sniff = Capture.new(:iface => iface, :start => true)
	puts "Listening on " + iface
	sniff.stream.each do |p|
		pkt = Packet.parse p
		if pkt.is_ip?
			if pkt.is_tcp?

				#packet_info = [pkt.ip_saddr, pkt.ip_daddr, pkt.size, pkt.proto.last]	#get packet info into struct for printing
				#puts "%-15s -> %-15s %-4d %s" % packet_info	#print basic info about every packet

				TCP_Scans(pkt)	#check for NMAP TCP scans
				NMAP_Scan(pkt)

				data = pkt.tcp_header.body	#create string from packet body to analyze

				creditCard(data, pkt)	#check for leaked plaintext credit cards
				passwords(data, pkt)	#check for leaked plaintext passwords
				XSS_Scan(data, pkt)		#check for XSS
			end
		end	#end IP 
	end # end sniff
end # end method


#main
startAlarm("en0")
