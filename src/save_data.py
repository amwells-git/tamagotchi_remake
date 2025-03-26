# define and return a json object to be saved to file
def save_data(age, # int
              stage, # str from ["egg", "baby", "child", "teen", "adult", "adult_spec"]
              start_time, # rounded time.time()
              elapsed_time, # long/int
              save_time, # rounded time.time()
              hunger, # int [0,4]
              happy, # int [0,4]
              discipline, # int [0,4]
              weight, # int [1,]
              poo, # int [0,] number of poo on screen
              last_poo, # rounded time.time() of last time poo was increased
              sick, # int [0,2] sickness level
              teen_ver, # int [1,2]
              adult_ver, # int [1,6]
              dead, # bool
              want_attention, # bool
              current_wants, # {str,} each string is a specific want from ['hungry', 'unhappy', 'sick', 'sleepy', 'fake']
              asleep, # bool
              sleep_start, # [18, 23] when sleep time starts, from datetime
              sleep_end, # [0, 8] when sleep time ends, from datetime
              light # bool
              ):
    return {
        "age": age,
        "stage": stage,
        "start_time": start_time,
        "elapsed_time": elapsed_time,
        "save_time": save_time,
        "hunger": hunger,
        "happy": happy,
        "discipline": discipline,
        "weight": weight,
        "poo": poo,
        "last_poo": last_poo,
        "sick": sick,
        "teen_ver": teen_ver,
        "adult_ver": adult_ver,
        "dead": dead,
        "want_attention": want_attention,
        "current_wants": current_wants,
        "asleep": asleep,
        "sleep_start": sleep_start,
        "sleep_end": sleep_end,
        "light": light
    }