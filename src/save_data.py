# define and return a json object to be saved to file
# int, long, int[0,4], int[0,4], int[0,4], int[1,], int[1,], bool, int[1,2], int[1,6], bool, bool, bool
def save_data(age, start_time, save_time, hunger, happy, discipline, weight, poo, sick, teen_ver,adult_ver, dead, want_attention, asleep):
    return {
        "age": age,
        "start_time": start_time,
        "save_time": save_time,
        "hunger": hunger,
        "happy": happy,
        "discipline": discipline,
        "weight": weight,
        "poo": poo,
        "sick": sick,
        "teen_ver": teen_ver,
        "adult_ver": adult_ver,
        "dead": dead,
        "want_attention": want_attention,
        "asleep": asleep
    }