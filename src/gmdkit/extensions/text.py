
def font_load(path) -> dict:
    
    result = {}
    
    file = open(path, "r")
        
    for line in file:
        
        tokens = line.split()
        first = tokens.pop(0)
        data = {}

        for t in tokens:

            k,v = t.split("=",maxsplit=1)
            
            if len(v) >= 2 and v[0] == v[-1] and v[0] in {'"', "'"}:
                v = v[1:-1]
            
            else:
                for cast in (int, float):
                    try:
                        v = cast(v)
                        break
                    except ValueError:
                        continue
            
            data[k] = v
        
        match first:
            case "page":
                pages = result.setdefault("pages",{})
                page_id = data.pop("id")
                pages[page_id] = data
            
            case "chars":
                result["chars_count"] = data.pop("count")
                
            case "char":
                chars = result.setdefault("chars",{})
                char_id = data.pop("id")
                chars[char_id] = data
            
            case "kernings":
                result["kernings_count"] = data.pop("count")
            
            case "kerning":
                kernings = result.setdefault("kernings",{})
                first_id = data.pop("first")
                second_id = data.pop("second")
                
                k_first = kernings.setdefault(first_id,{})
                k_first[second_id] = data.pop("amount")
                chars[char_id] = data
                
            case _:
                result[first] = data
                
    file.close()
        
    return result


if __name__ == "__main__":
    font = font_load(r"E:\SteamLibrary\steamapps\common\Geometry Dash\Resources\bigFont-uhd.fnt")


        
            
    