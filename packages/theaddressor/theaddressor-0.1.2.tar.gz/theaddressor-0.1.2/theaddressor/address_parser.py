import re
import json

class AddressParser:
    US_ZIP_REGEX = re.compile(r'^\d{5}(-\d{4})?$')
    CA_ZIP_REGEX = re.compile(r'^[A-Za-z]\d[A-Za-z][ ]?\d[A-Za-z]\d$')  # Handles optional space in Canadian ZIPs
    PHONE_REGEX = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    EMAIL_REGEX = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
    REF_REGEX = re.compile(r'\b(?:PO|P\.O\.|Invoice|Inv|Ref(?:erence)?|RMA|SO|Order)\s*#?\s*\w+', re.IGNORECASE)
    URL_REGEX = re.compile(r'https?://[^\s]+', re.IGNORECASE)

    STATE_ABBR = {
        'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
        'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
        'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY','DC','PR','GU','VI','AS','MP',
        'AB', 'BC','MB','NB','NL','NS','NT','NU','ON','PE','QC','SK','YT',    }

    STREET_SUFFIXES = {
        "aly", "alley",
        "anx", "annex",
        "arc", "arcade",
        "ave", "avenue", "av", "avenu", "avn", "avenu", "avenu", "avenu",
        "byu", "bayou",
        "bch", "beach",
        "bend",
        "blf", "bluff", "bluffs",
        "blvd", "boulevard", "boulv",
        "bnd", "bend",
        "br", "branch",
        "brg", "bridge",
        "brk", "brook", "brooks",
        "bg", "burg", "bgs", "burghs",
        "byp", "bypass", "by-pass", "bypas",
        "cp", "camp",
        "cyn", "canyon", "canyn", "cyn",
        "cpe", "cape",
        "cswy", "causeway", "causewy", "cswy", "causwa",
        "ctr", "center", "cent", "centr", "centre", "cnter", "cntr",
        "cir", "circle", "circ", "circl", "crcl", "crcle",
        "clfs", "cliffs",
        "clb", "club",
        "cmn", "common",
        "cor", "corner", "corners",
        "cors", "corners",
        "crse", "course",
        "ct", "court",
        "cv", "cove", "coves",
        "crk", "creek",
        "cres", "crescent",
        "xing", "crossing",
        "dl", "dale",
        "dm", "dam",
        "dr", "drive", "drv",
        "dv", "divide",
        "est", "estate", "estates",
        "expy", "expressway", "exp", "expr", "express", "expw",
        "ext", "extension", "extn", "extnsn",
        "fls", "falls", "fall",
        "flt", "flat", "flats",
        "frd", "ford",
        "frg", "forge",
        "frk", "fork", "forks",
        "frst", "forest", "frst",
        "fwy", "freeway", "frway", "frwy",
        "gtwy", "gateway", "gatewy", "gatway", "gtway",
        "gln", "glen", "glens",
        "grn", "green", "grns",
        "grv", "grove", "groves",
        "hbr", "harbor", "harbors", "hrbor", "harbr", "harb",
        "hl", "hill",
        "hls", "hills",
        "holw", "hollow", "hllw", "holws",
        "hn", "haven",
        "hvn", "haven",
        "hts", "heights", "highway",
        "hwy", "highway", "hiway", "hiwy", "hway", "hwy",
        "inlt", "inlet",
        "is", "island",
        "isle", "isles", "islnd",
        "jct", "junction", "jction", "jctn", "junctn", "juncton",
        "ky", "key", "keys",
        "knl", "knoll", "knolls",
        "lndg", "landing", "lndng",
        "ln", "lane",
        "lgt", "light",
        "lgts", "lights",
        "loop",
        "mall",
        "mnr", "manor",
        "mdw", "meadow", "meadows", "mdws",
        "msn", "mission", "missn", "mssn",
        "mtwy", "motorway",
        "mt", "mount",
        "nck", "neck",
        "orch", "orchard",
        "oval",
        "opas", "overpass",
        "park", "parks",
        "pkwy", "parkway", "parkwy", "pkway", "pky", "pkwys",
        "pass",
        "path",
        "pike", "pikes",
        "pne", "pine", "pines",
        "pl", "place",
        "plz", "plaza", "plza",
        "pt", "point", "pts", "points",
        "pr", "prairie",
        "radl", "radial",
        "ramp",
        "rnch", "ranch", "ranches", "rnchs",
        "rdg", "ridge", "rdge",
        "rd", "road", "rd.", "roads",
        "rte", "route",
        "row",
        "rue",
        "run",
        "shl", "shoal", "shoals",
        "shr", "shore", "shores",
        "shrs", "shores",
        "skwy", "skyway",
        "smt", "summit",
        "spg", "spring", "spgs", "sprngs",
        "sq", "square", "sqr", "sqre", "squ", "sqs",
        "sta", "station", "statn", "stn",
        "stra", "stravenue", "strav", "straven", "stravn", "strvn", "strvnue",
        "strm", "stream",
        "st", "street", "str", "st.",
        "ter", "terrace",
        "trce", "trace",
        "trak", "track",
        "trfy", "trafficway",
        "trl", "trail", "trails", "trl.",
        "tunl", "tunnel", "tunel", "tunls", "tunnl", "tunnle",
        "tpke", "turnpike", "trnpk", "turnpk",
        "upas", "underpass",
        "un", "union", "unions",
        "vly", "valley", "valleys",
        "vis", "vista", "vist", "vsta",
        "walk", "walks",
        "wall",
        "way", "wy", "ways",
        "wl", "well",
        "xing", "crossing",
        "xrd", "crossroad",
        "xtn", "extension",
        "sr",
    }


    HIGHWAY_REGEX = re.compile(r'\b(I|US|SR|Hwy|Highway|Route|Rte)\s?[-]?\s?\d+\b', re.IGNORECASE)
    ADDRESS_REGEX = re.compile(r'\d+\s+[A-Za-z0-9\s\.,#-]+')
    NAME_REGEX = re.compile(r"^[A-Za-z][A-Za-z\.'\-]*?(?:\s[A-Za-z][A-Za-z\.'\-]*){0,5}$")


    def _contains_street_suffix(self, text):
        words = set(word.lower() for word in text.split())
        return bool(words & self.STREET_SUFFIXES)

    def _is_us_zip(self, text):
        return bool(self.US_ZIP_REGEX.fullmatch(text))

    def _is_ca_zip(self, text):
        return bool(self.CA_ZIP_REGEX.fullmatch(text))

    def _is_zip(self,text):
        return (self._is_us_zip(text) or self._is_ca_zip(text))

    def _looks_like_location_line(self, line):
        cleaned = line.replace(",", " ").strip()
        parts = cleaned.split()
        
        if len(parts) >= 2:
            maybe_zip = parts[-1]
            maybe_state = parts[-2].upper() if self._is_us_zip(maybe_zip) or self._is_ca_zip(maybe_zip) else parts[-1].upper()
            if maybe_state in self.STATE_ABBR:
                return True
        return False

    def _looks_like_address_line(self, line):
        return (
            self.HIGHWAY_REGEX.search(line)
            or self._contains_street_suffix(line)
            or bool(re.match(r'^\d+', line.strip()))
        )

    
    def __init__(self, lines,debug=None):
        self.debug=debug
        STAGE_NAME = 0
        STAGE_ADDRESS1 = 1
        STAGE_ADDRESS2 = 2
        STAGE_LOCATION = 3
        STAGE_ZIPCODE = 4
        STAGE_COMPLETE = 5


        result = {
            "name": [],
            "company": "",
            "address1": "",
            "address2": "",
            "city": "",
            "state": "",
            "zipcode": "",
            "country": "",
            "phone": [],
            "email": [],
            "reference": [],
            "url": [],
            "unknown": []
        }

        # cleanup and assignment
        tagged = []
        if self.debug: print(lines)
        tagged = []
        for line in lines:
            line = re.sub(r'HWYSTE', 'HWY STE', line)
            tag = 'unknown'
            if self.EMAIL_REGEX.search(line):
                tag = 'email'
            elif self.URL_REGEX.search(line):
                tag = 'url'
            elif self.PHONE_REGEX.search(line):
                tag = 'phone'
            elif self.REF_REGEX.search(line):
                tag = 'reference'
            elif self._looks_like_location_line(line):
                line = line.replace(',', ' ')
                tag = 'location'
            elif self._looks_like_address_line(line):
                tag = 'address'
            elif self._is_zip(line):
                line = line.replace(',', ' ')
                tag = 'zip'
            elif "suite" in line.lower() or "ste" in line.lower() or "#" in line.lower():
                tag = 'suite'
            elif self.NAME_REGEX.fullmatch(line.strip()):
                tag = 'name_candidate'
            
            tagged.append((line.lower().strip(), tag))

        # Move name_candidate before address/suite/location if found after them
        name_idx = next((i for i, (_, tag) in enumerate(tagged) if tag == 'name_candidate'), None)
        insert_before_idx = next((i for i, (_, tag) in enumerate(tagged) if tag in {'address', 'suite', 'location'}), None)

        if name_idx is not None and insert_before_idx is not None and name_idx > insert_before_idx:
            tagged.insert(insert_before_idx, tagged.pop(name_idx))

        if self.debug: print(tagged)

        index=0
        stage = STAGE_NAME
        for tagged_line in tagged:
            index+=1
            line = tagged_line[0] 
            tag = tagged_line[1]
            if self.debug: print(tag,line)
            if not line:
                continue


            if tag=="url":
                result["url"].append(self.URL_REGEX.search(line).group())
                continue

            if tag=="email":
                result["email"].append(self.EMAIL_REGEX.search(line).group())
                continue

            if tag=="phone":
                result["phone"].append( self.PHONE_REGEX.search(line).group())
                continue

            if tag=="reference":
                result["reference"].append(self.REF_REGEX.search(line).group())
                continue

            
            if tag=="zip":
                if self._is_us_zip(line): 
                    result["zipcode"] = self.US_ZIP_REGEX.search(line).group()
                    result["country"] ="US"
                if self._is_ca_zip(line): 
                    result["zipcode"] = self.CA_ZIP_REGEX.search(line).group()
                    result["country"] ="CANADA"
                continue


            if stage == STAGE_NAME:
                if self.debug: print("In NAME",line)
                if tag in {'address', 'suite',}:
                    tagged.insert(0, (line, tag))
                    stage = STAGE_ADDRESS1
                    if self.debug: print("Moving to Address")
                    continue
                elif tag in {'email', 'phone', 'reference', 'url'}:
                    continue  # Skip structured fields from name
                else:
                    if self.debug: print("Got Name",line)
                    result['name'] .append(line.strip())
                    continue


            if stage == STAGE_ADDRESS1:
                if self.debug: print("In Address 1",line)

                if self._looks_like_address_line(line):
                    if self.debug: print("SET ADDRESS 1")
                    result["address1"] = line
                    stage = STAGE_ADDRESS2
                    continue
                else:
                    if self.debug: print("UNKNOWN")
                    result["unknown"].append(line)
                    continue

            if stage == STAGE_ADDRESS2:
                if self.debug: print("In Address 2")
                if self._looks_like_location_line(line):
                    stage = STAGE_LOCATION
                    tagged.insert(0, (line,tag))
                    if self.debug: print("Move to Location")
                    continue
                else:
                    result["address2"] = line
                    stage = STAGE_LOCATION
                    if self.debug: print("Got Address 2Move to Location")
                    continue
                

            if stage == STAGE_LOCATION:
                if self.debug: print("In Location",line)

                parts = line.split()
                if len(parts) >= 2:
                    maybe_zip = parts[-1]
                    if self.debug: print("---",maybe_zip)
                    part_index=-2
                    is_zip=None
                    is_us_zip = self._is_us_zip(maybe_zip)
                    is_can_zip=None
                    if len(parts[-2])==3 and len(parts[-1])==3:
                        maybe_zip=f"{parts[-2]}{parts[-1]}"
                        if self.debug: print("-IN SPLIT--",maybe_zip)
                        is_can_zip=self._is_ca_zip(maybe_zip)
                        part_index=-3
                    elif len(maybe_zip)==6:
                        is_can_zip=self._is_ca_zip(maybe_zip)
                    
                    if is_us_zip:
                        if self.debug: print("IS US")
                        is_zip=is_us_zip
                    
                    if is_can_zip:
                        if self.debug: print("IS CAN")
                        is_zip=is_can_zip

                    
                    maybe_state = parts[part_index].upper()
                    is_state = maybe_state in self.STATE_ABBR
                    maybe_city = ' '.join(parts[:part_index]) if len(parts) > 2 else ''

                    if is_state:
                        result["zipcode"] = maybe_zip
                        result["state"] = maybe_state
                        result["city"] = maybe_city
                        if self._is_ca_zip(maybe_zip): 
                            result["zipcode"] = maybe_zip
                            result["country"] = "Canada" 
                            result["zipcode_valid"] = True

                        elif self._is_us_zip(maybe_zip): 
                            result["country"] ="US"
                            result["zipcode_valid"] = True

                        else: 
                            #result["zipcode"] = None
                            result["country"] = None
                            result["zipcode_valid"] = False

                        stage = STAGE_COMPLETE
                        continue
                    else:
                        maybe_state = parts[-1]
                        is_state = maybe_state.upper() in self.STATE_ABBR
                    
                    if is_state:
                        maybe_city = ' '.join(parts[:-1])
                        result["state"] = maybe_state
                        result["city"] = maybe_city
                        stage = STAGE_ZIPCODE
                        continue
                    else:
                        result['unknown'].append(line)
                        continue

            if stage == STAGE_ZIPCODE:
                maybe_zip = line.strip()

                if len(maybe_zip) == 3 and maybe_zip.isalnum() and index < len(tagged):
                    next_line, next_tag = tagged.pop(index)
                    next_zip_part = next_line.strip()
                    combined_zip = maybe_zip + next_zip_part

                    if self._is_ca_zip(combined_zip):
                        result["zipcode"] = combined_zip
                        result["country"] = "Canada"
                        result["zipcode_valid"] = True
                        stage = STAGE_COMPLETE
                        continue
                    else:
                        # Push back if invalid
                        tagged.insert(index, (next_line, next_tag))

                # Handle as standalone ZIP
                result["zipcode"] = maybe_zip
                stage = STAGE_COMPLETE

                if self._is_ca_zip(maybe_zip):
                    result["country"] = "Canada"
                    result["zipcode_valid"] = True
                elif self._is_us_zip(maybe_zip):
                    result["country"] = "US"
                    result["zipcode_valid"] = True
                else:
                    result["country"] = None
                    result["zipcode_valid"] = False
                    result["unknown"].append(line)
                
            if stage == STAGE_COMPLETE and (self._looks_like_address_line(line) or self._looks_like_location_line(line)):
                break

        if len(result['name'])>1:
            tokens=result['name']
            result['name']=tokens[0]
            result['company']='\'n'.join(tokens[1:])
        elif len(result['name'])==1:
                result['name']=result['name'][0]
        else:
            result['name']=''
        
        # fix foramtting
        for key in result:
            if key in ('url','email','reference','phone'):
                continue
            if isinstance(result[key], str):
                words = result[key].split()
                formatted = []
                for word in words:
                    if len(word) == 2:
                        formatted.append(word.upper())
                    else:
                        formatted.append(word.capitalize())
                result[key] = ' '.join(formatted)


        self.result=result
        if self.debug: print(json.dumps(result, indent=2))


    def get(self):
        return self.result




