#!/usr/bin/python
# coding=utf-8

import os
import sys
import time
import datetime
from optparse import OptionParser

from httplib2 import Http
from urllib import urlencode
from datetime import datetime

import subprocess

# see end of file for defenitions
ticker_map = None
categories = None

def parse_date(string):
	return datetime.strptime(string, "%Y-%m-%d")

def date_string(date):
	return date.strftime("%d.%m.%Y")

def get_ticker_id(ticker):
	ticker = ticker.upper()
	# what about a find(list, key=) ???
	for cell in ticker_map:
		if cell[1] == ticker:
			return cell[0]
	raise "no_such_ticker"
	
def main():
	parser = OptionParser("%prog [options] <LOG> <entry>")
	parser.add_option("-f", "--from", default=None,
			help="start date (incl.)")
	parser.add_option("-t", "--to", default=None,
			help="end date (incl.)")
	parser.add_option("-T", "--ticker", default="0",
			help="")
	parser.add_option("-c", "--category", default="-1",
			help="numeric id, use -p")
	parser.add_option("-o", "--out", default="-")
	parser.add_option("-p", "--print-category", action="store_true", default=False,
			help="")
	options, args = parser.parse_args()
	
	if options.print_category:
		for c in categories:
			print c
		return

	from_param = parse_date(getattr(options, "from")) if getattr(options, "from") != None else datetime.now()
	to_param = parse_date(options.to) if options.to != None else datetime.now()

	post_params = {
"selectedPagenumber":"0",
"searchSubmitType":"searchtype.full",
"searchtype":"",
"searchCriteria.issuerId":get_ticker_id(options.ticker),
"searchCriteria.instrumentId":"-1",
"searchCriteria.issuerSign":"FOE",
"searchCriteria.categoryId":"-1",
"searchCriteria.fromDate":from_param,
"searchCriteria.toDate":to_param,
"_searchCriteria.infoRequiredOnly":"",
"_searchCriteria.oamMandatoryOnly":"",
"_searchCriteria.currentVersionOnly":"",
"_searchCriteria.activeIssuersOnly":"",
"searchCriteria.activeIssuersOnly":"true"
}
	post_data = urlencode(post_params) 

	subprocess.call(["wget", "-O", options.out, "--post-data", post_data, "http://www.newsweb.no/newsweb/search.do"])

	# whoooo.. for some reason httplib2 and newsweb are not best friends...
	#http = Http()
	#resp, content = http.request("http://www.newsweb.no/newsweb/search.do", "POST", urlencode(postParams))
	#datetime.strptime(options.time, "%H:%M")

# hopefully these doesn't change to often

categories = [("114", "ANDRE BØRSMELDINGER"), 
("96", "AUKSJONSKALENDER KORTE STATSPA"), 
("101", "AUKSJONSKALENDER STATSOBLIGASJ"), 
("109", "AVTALER"), 
("87", "BØRSPAUSE"), 
("119", "DERIVATMELDINGER"), 
("62", "EKS.DATO"), 
("63", "FINANSIELL KALENDER"), 
("122", "FINANSIELL RAPPORTERING"), 
("64", "FISJON / FUSJON"), 
("65", "FLAGGING"), 
("68", "GENERALFORSAMLINGSINFO"), 
("125", "IKKE-INFORMASJONSPLIKTIGE PRESSEMELDINGER"), 
("70", "INDEKSINFORMASJON"), 
("128", "INFORMASJON FRA ANDRE AKTØRER"), 
("124", "INFORMASJON FRA OSLO BØRS"), 
("71", "KAPITALENDRINGER / UTBYTTEOPPLYSNINGER"), 
("73", "MELDEPLIKTIG HANDEL"), 
("200", "MELDING FRA FINANSTILSYNET"), 
("74", "NOTERING AV VERDIPAPIRER"), 
("94", "NYHETER1"), 
("95", "NYHETER2"), 
("75", "OBLIGASJONSHENDELSER"), 
("76", "OPPKJØP"), 
("120", "PETROLEUM RESERVER"), 
("81", "PROSPEKT"), 
("98", "RESULTAT KORTE STATSPAPIRER"), 
("103", "RESULTAT STATSOBLIGASJONER"), 
("115", "RESULTATUTSIKTER"), 
("82", "SUSPENSJONER"), 
("93", "SÆRLIG OBSERVASJON"), 
("117", "SØKNAD"), 
("102", "UTLEGGELSE AV STATSOBLIGASJONE"), 
("97", "UTLEGGELSE KORTE STATSPAPIRER "), 
("123", "UTVIDET MELDING/INFORMASJONSDOKUMENT"), 
("127", "VEDTAK"), 
("121", "ÅRSOVERSIKT")]

ticker_map = [['-1', None],
['8380','TFSO'],
['8105','AASB'],
['11262','SMF'],
['2017','ASC'],
['6806','ACTA'],
['6051','AFG'],
['6772','AEN'],
['8128','AGR'],
['6047','AKER'],
['6101','AKBM'],
['8006','AKD'],
['8462','AKPS'],
['7924','AKS'],
['7765','AKSO'],
['6093','NYSK'],
['6771','AKKR'],
['6083','AIK'],
['8194','AKVA'],
['8252','ALGETA'],
['7954','AMSC'],
['7072','APP'],
['8465','ABT'],
['11216','ARCHER'],
['8036','ARSP'],
['1007','AFK'],
['11249','AOD'],
['1957','AKO'],
['8069','ASKSB'],
['2305','ATEA'],
['6131','AURG'],
['8163','AUSS'],
['8573','AVINOR'],
['11178','AVM'],
['11244','AWDR'],
['11268','ALNG'],
['8360','BXPL'],
['8620','BAKKA'],
['8418','BLSG'],
['6114','BOSL'],
['11260','bankn'],
['2221','BEL'],
['8495','BERGEN'],
['1517','BEKO'],
['6278','BKK'],
['8481','SBBIG'],
['6339','BIONOR'],
['7963','BIOTEC'],
['7150','BIRD'],
['11197','BLSB'],
['2230','BLO'],
['8529','BLH'],
['1946','BNB'],
['8515','BNBO'],
['11300','BOA'],
['6159','BNKR'],
['2208','BON'],
['2209','BOR'],
['8524','BIND'],
['8307','BOUVET'],
['8631','BRIDGE'],
['8538','BFSBG'],
['11182','SSFBK'],
['8108','BWO'],
['8045','BWG'],
['6049','BMA'],
['8496','CSOL'],
['8316','CECON'],
['11205','CELL'],
['7960','CEQ'],
['8109','CLAVIS'],
['8165','COD'],
['7766','COLG'],
['8243','COMROD'],
['6006','COV'],
['8238','COP'],
['11293','CRUDE'],
['11179','DMABB'],
['6085','DAT'],
['11299','DEED'],
['8227','DESSC'],
['2098','NST'],
['8376','DETNOR'],
['11302','DFDS'],
['7795','DIAG'],
['11240','DISC'],
['1772','DNB'],
['7834','DNBKAP'],
['1827','DNBA'],
['11184','DNBNB'],
['1015','DNO'],
['8398','DOCK'],
['6489','DOF'],
['7984','DOFSUB'],
['8062','DOLP'],
['6803','DOM'],
['8492','DSB'],
['8498','DSBS'],
['6137','ECEN'],
['7942','EIOF'],
['8068','EIEN'],
['1675','EIKR'],
['8196','ECHEM'],
['6072','EMS'],
['2520','EKO'],
['101283667','EKSPFI'],
['8264','EMGS'],
['6136','ELT'],
['7828','ENBU'],
['7610','ENEID'],
['8390','EOC'],
['11204','EQO'],
['11303','ETNE'],
['11266','ETRION'],
['6176','EVRY'],
['7981','FAIR'],
['6025','FSB'],
['8627','FSBKR'],
['8016','FARA'],
['2255','FAR'],
['1268','FKOV'],
['100000103','FT'],
['8510','FVA'],
['5181','FJELL'],
['8594','FLNG'],
['8399','FOSB'],
['8412','FBU'],
['6063','FOE'],
['8317','FOP'],
['6117','FRO'],
['7997','FUNCOM'],
['2207','GRO'],
['7837','RISH'],
['8285','GJEB'],
['11177','GJBB'],
['11217','GJF'],
['11279','GLRIG'],
['6802','GOL'],
['7823','GOGL'],
['2312','GOD'],
['2319','GRR'],
['8362','GSF'],
['2269','GYL'],
['1937','HAFS'],
['7918','HAFO'],
['2499','HGSB'],
['7928','HAVI'],
['11212','HESB'],
['8616','HEBK'],
['6053','HELG'],
['5067','HELK'],
['5203','HEX'],
['6746','HJGSB'],
['8054','HJSB'],
['11251','HLNG'],
['11280','HBC'],
['6130','HOLG'],
['6171','HSPG'],
['6745','HOSB'],
['8067','HRG'],
['6002','IMSK'],
['8606','IDEX'],
['6084','IGE'],
['7917','IMAREX'],
['5202','ISSG'],
['8446','INFRA'],
['8135','IOX'],
['8201','ITX'],
['6153','ITE'],
['11192','JLA'],
['7780','JSHIP'],
['8096','JESB'],
['2446','JIN'],
['6098','KIT'],
['6483','KLEG'],
['11298','KLPB'],
['11207','KLPKK'],
['5021','KOLL'],
['1172','KOMB'],
['7941','KOA'],
['2331','KOG'],
['8106','KRASB'],
['7781','KFS'],
['11219','KGLED'],
['11252','KVAER'],
['8150','KDSB'],
['7169','LAKRB'],
['11228','LANDKBK'],
['6148','LAKO'],
['6045','LBSB'],
['7148','LSG'],
['11210','LISB'],
['8090','LSTSB'],
['8140','LSSB'],
['11254','LUSB'],
['7616','LYSE'],
['5063','MHG'],
['7774','MEDI'],
['11231','MDSB'],
['6147','MELG'],
['8100','MODSB'],
['8628','MOBK'],
['11187','MORPOL'],
['2311','NAM'],
['8447','NATTO'],
['8063','NAVA'],
['6143','NESG'],
['11180','NETCO'],
['8279','NEXUS'],
['7829','NIO'],
['11261','NJGI'],
['8477','NTEH'],
['1198','NTFY'],
['7994','NORD'],
['1103','NODA'],
['1612','NOKR'],
['11273','NOFIN'],
['8123','NOM'],
['5117','NOD'],
['1559','NORLK'],
['100000101','NB'],
['7798','NORG'],
['6102','NEC'],
['1114','NHY'],
['11230','NRK'],
['2498','NSG'],
['8605','NORTH'],
['8373','NLPR'],
['6497','NOF'],
['11292','NORES'],
['8166','NAUR'],
['7930','NORT'],
['8504','NPEL'],
['11235','NRS'],
['7628','NAS'],
['2370','NOCC'],
['8416','NOR'],
['8191','NPRO'],
['8241','OBLIV'],
['8236','OBLV'],
['8629','OBFB'],
['11277','OCR'],
['8229','OTS'],
['11211','ODAL'],
['2366','ODF'],
['1308','OLT'],
['11232','OLSH'],
['11198','OPSB'],
['7759','OPERA'],
['5173','ORO'],
['8035','OSPA'],
['1107','ORK'],
['8197','ORLSB'],
['100000102','--'],
['6335','OBOS'],
['100000100','-'],
['1205','OSLKO'],
['8029','OSEN'],
['8624','PEN'],
['8596','PARB'],
['8502','PCIB'],
['2342','PGS'],
['6018','PDR'],
['6357','PHO'],
['11183','PLBK'],
['8582','PLCS'],
['8537','POL'],
['8497','POSTEN'],
['8410','PRON'],
['6010','PRS'],
['11226','PROS'],
['8322','PROTCT'],
['6793','PSI'],
['7065','QFR'],
['7938','QEC'],
['8270','REM'],
['8080','REC'],
['8224','REPANT'],
['8002','RXT'],
['2348','RIE'],
['2459','RGT'],
['8353','ROM'],
['6046','RCL'],
['11233','SDSD'],
['11191','SAGA'],
['8288','SALM'],
['5024','SADG'],
['11208','SANC'],
['1387','SAS'],
['5059','SCI'],
['8298','SCAN'],
['2354','SCH'],
['8025','SBX'],
['7968','SDRL'],
['8046','SELB'],
['6749','SESB'],
['11291','SBO'],
['8083','SELV'],
['11243','SEVDR'],
['7820','SEVAN'],
['11234','SHBS'],
['11225','SFLN'],
['7956','SIOFF'],
['6776','SSI'],
['6737','SINO'],
['7882','SEB'],
['2369','SKI'],
['11199','SKASB'],
['1638','SFEN'],
['11304','SOGSB'],
['6066','SOFF'],
['8592','SOREII'],
['2367','SOLV'],
['8626','STRANS'],
['8022','SONG'],
['11271','SORB'],
['8379','SPBKR'],
['2352','SBVG'],
['7950','SBGRP'],
['8206','SBGG'],
['8245','SBHA'],
['11265','SBNK'],
['1972','NONG'],
['1823','NVSB'],
['1248','NTSG'],
['5195','SOAG'],
['5125','RING'],
['1695','MING'],
['6007','SBSS'],
['1797','SRBANK'],
['5204','SBHE'],
['1652','MORG'],
['6484','NASB'],
['1636','SPOG'],
['11194','SPOBK'],
['1814','PLUG'],
['6065','SFSB'],
['1810','SORG'],
['8332','SBTE'],
['1642','SVEG'],
['8543','SBVB'],
['11193','SPSK'],
['8507','SPU'],
['8364','SPYDG'],
['8634','SSBB'],
['11284','STHY'],
['7800','STAEN'],
['5009','STATKR'],
['5099','STANE'],
['1309','STL'],
['11206','SFR'],
['2378','SST'],
['5097','SNI'],
['1955','STB'],
['1821','STORB'],
['8509','STORK'],
['148','STORL'],
['8576','STMS'],
['11189','STORM'],
['8257','STSB'],
['7775','STXEUR'],
['6030','SUBC'],
['11200','SUSB'],
['5033','SHB'],
['7880','SWED'],
['8602','SWHO'],
['6111','TAK'],
['11227','TOP01'],
['6233','TEL'],
['8112','TELIO'],
['8001','TBK'],
['11201','TEGR'],
['6070','TGS'],
['8623','SSC'],
['8458','THIN'],
['6774','THOL'],
['2272','TIDE'],
['6485','TMSB'],
['7959','TINE'],
['6759','TNSB'],
['2392','TOM'],
['1662','TOTG'],
['11236','TSBK'],
['8251','TSU'],
['8070','TRGSB'],
['1801','TRBO'],
['5010','TROEN'],
['1214','TRKO'],
['2525','TTS'],
['11295','UMAR'],
['7833','VARD'],
['11256','VASA'],
['8539','VHSBG'],
['2400','VEI'],
['11202','VEBK'],
['11294','VPOS'],
['8152','VJBA'],
['8186','VEEN'],
['2402','VSS'],
['7923','VIZ'],
['2403','VVL'],
['7953','WRL'],
['11186','WWASA'],
['2405','WWI'],
['7915','WILS'],
['7760','YAR'],
['8383','ZONC']]

if __name__ == "__main__":
	main()
