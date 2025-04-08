from tqdm import tqdm
import os
import gc
from subdomain_permut.utility import dedupe_file, memory_load_test, append_file

class SimplePermut:
    def permut_sub_dot_sub(args, keywords) -> None:
        """
        generate permutations for {sub}.{sub} method
        """
        if args.verbose:
            print('[*] Generating {sub}.{sub} permutations')

        with open(args.output, 'a') as file:
            # sub.domain
            for keyword in tqdm(keywords, desc="[*] Initial permutation"):
                file.write(f"{keyword}.{args.domain}\n")
        
        if args.level == 1:
            return
        
        # max array size for in-memory buffer
        max_arr_length = memory_load_test(args)
            
        # dedupe file
        dedupe_file(args.output)

        # generate next levels of permutation
        buffer_array = []
        for _ in range(args.level-1):
            if args.verbose:
                print(f'[*] Starting level {_+2}')
            # empty buffer array if any exist
            if len(buffer_array) != 0:
                if args.verbose:
                    print(f'[*] Clearing buffer from previous iteration')
                with open(args.output, 'a') as f:
                    f.writelines(buffer_array)
                del buffer_array
                gc.collect()
                buffer_array = []
            # read through previous level permut and add subs
            with open(args.output, 'r') as existing_file:
                for subdomain in tqdm(existing_file, desc=f'[*] Level {_+2}'):
                    subdomain = subdomain.rstrip()
                    for keyword in keywords:
                        buffer_array.append(f"{keyword}.{subdomain}\n")
                        if len(buffer_array) > max_arr_length:
                            with open(f'.{args.output}', 'a') as f: # write to temp file instead of main file
                                f.writelines(buffer_array)
                            del buffer_array
                            gc.collect()
                            buffer_array = []
            
            # flush buffer array
            if len(buffer_array) != 0:
                with open(f'.{args.output}', 'a') as f:
                    f.writelines(buffer_array)
                del buffer_array
                gc.collect()
                buffer_array = []
            
            # write contents of temporary file into main file
            append_file(f'.{args.output}', args.output)

            # remove temporary file
            os.remove(f'.{args.output}')
        
            # flush buffer array
            if len(buffer_array) != 0:
                with open(args.output, 'a') as f:
                    f.writelines(buffer_array)
                del buffer_array
                gc.collect()
                buffer_array = []
            if args.verbose:
                print(f'[*] All temporary resources freed by level {_+2}')

    def permut_sub_sub(args, keywords) -> None:
        """
        generate permutations for {sub}{sub} method
        """
        if args.verbose:
            print('[*] Generating {sub}{sub} permutations')
        
        with open(args.output, 'a') as file:
            # subsub.domain
            for keyword1 in tqdm(keywords, desc="[*] Initial permutation"):
                for keyword2 in keywords:
                    file.write(f"{keyword1}{keyword2}.{args.domain}\n")
        
        if args.level == 1:
            return
        
        # max array size for in-memory buffer
        max_arr_length = memory_load_test(args)

        # dedupe file
        dedupe_file(args.output)

        # generate next levels of permutation
        buffer_array = []
        for _ in range(args.level-1):
            if args.verbose:
                print(f'[*] Starting level {_+2}')
            
            # empty buffer array if any exist
            if len(buffer_array) != 0:
                if args.verbose:
                    print(f'[*] Clearing buffer from previous iteration')
                with open(args.output, 'a') as f:
                    f.writelines(buffer_array)
                del buffer_array
                gc.collect()
                buffer_array = []
            
            # read through previous level permut and add subs
            with open(args.output, 'r') as existing_file:
                for subdomain in tqdm(existing_file, desc=f'[*] Level {_+2}'):
                    subdomain = subdomain.rstrip()
                    for keyword1 in keywords:
                        keyword1 = keyword1.rstrip()
                        for keyword2 in keywords:
                            keyword2 = keyword2.rstrip()
                            buffer_array.append(f"{keyword1}{keyword2}.{subdomain}\n")
                            if len(buffer_array) > max_arr_length:
                                with open(f'.{args.output}', 'a') as f: # write to temp file instead of main file
                                    f.writelines(buffer_array)
                                del buffer_array
                                gc.collect()
                                buffer_array = []

            # combination for "{keyword}.{keyword1}{keyword2}.{domain/subdomain}"
            with open(args.output, 'r') as existing_file:
                for subdomain in tqdm(existing_file, desc=f'[*] Level {_+2} - prepending sub'):
                    subdomain = subdomain.rstrip()
                    for keyword in keywords:
                        buffer_array.append(f"{keyword}.{subdomain}\n")
                        if len(buffer_array) > max_arr_length:
                                with open(f'.{args.output}', 'a') as f: # write to temp file instead of main file
                                    f.writelines(buffer_array)
                                del buffer_array
                                gc.collect()
                                buffer_array = []
            
            # flush buffer array
            if len(buffer_array) != 0:
                with open(f'.{args.output}', 'a') as f:
                    f.writelines(buffer_array)
                del buffer_array
                gc.collect()
                buffer_array = []
            
            # write contents of temporary file into main file
            append_file(f'.{args.output}', args.output)

            # remove temporary file
            os.remove(f'.{args.output}')
        
            # flush buffer array
            if len(buffer_array) != 0:
                with open(args.output, 'a') as f:
                    f.writelines(buffer_array)
                del buffer_array
                gc.collect()
                buffer_array = []
            if args.verbose:
                print(f'[*] All temporary resources freed by level {_+2}')
        
    def permut_sub_hyphen_sub(args, keywords) -> None:
        """
        generate permutations for {sub}-{sub}
        """

        if args.verbose:
            print('[*] Generating {sub}-{sub} permutation')
        
        with open(args.output, 'a') as file:
            # sub.domain
            for keyword1 in tqdm(keywords, desc="[*] Initial permutation"):
                for keyword2 in keywords:
                    file.write(f"{keyword1}-{keyword2}.{args.domain}\n")
        
        if args.level == 1:
            return
        
        # max array size for in-memory buffer
        max_arr_length = memory_load_test(args)
            
        # dedupe file
        dedupe_file(args.output)

        # generate next levels of permutation
        buffer_array = []
        for _ in range(args.level-1):
            if args.verbose:
                print(f'[*] Starting level {_+2}')
            
            # empty buffer array if any exist
            if len(buffer_array) != 0:
                if args.verbose:
                    print(f'[*] Clearing buffer from previous iteration')
                with open(args.output, 'a') as f:
                    f.writelines(buffer_array)
                del buffer_array
                gc.collect()
                buffer_array = []
            
            # read through previous level permut and add subs
            with open(args.output, 'r') as existing_file:
                for subdomain in tqdm(existing_file, desc=f'[*] Level {_+2}'):
                    subdomain = subdomain.rstrip()
                    for keyword1 in keywords:
                        for keyword2 in keywords:
                            buffer_array.append(f"{keyword1}-{keyword2}.{subdomain}\n")
                            if len(buffer_array) > max_arr_length:
                                with open(f'.{args.output}', 'a') as f: # write to temp file instead of main file
                                    f.writelines(buffer_array)
                                del buffer_array
                                gc.collect()
                                buffer_array = []
            
            # combination for "{keyword}.{keyword1}-{keyword2}.{domain/subdomain}"
            with open(args.output, 'r') as existing_file:
                for subdomain in tqdm(existing_file, desc=f'[*] Level {_+2} - prepending sub'):
                    subdomain = subdomain.rstrip()
                    for keyword in keywords:
                        buffer_array.append(f"{keyword}.{subdomain}\n")
                        if len(buffer_array) > max_arr_length:
                                with open(f'.{args.output}', 'a') as f: # write to temp file instead of main file
                                    f.writelines(buffer_array)
                                del buffer_array
                                gc.collect()
                                buffer_array = []
            
            # flush buffer array
            if len(buffer_array) != 0:
                with open(f'.{args.output}', 'a') as f:
                    f.writelines(buffer_array)
                del buffer_array
                gc.collect()
                buffer_array = []

            # write contents of temporary file into main file
            append_file(f'.{args.output}', args.output)

            # remove temporary file
            os.remove(f'.{args.output}')
        
            # flush buffer array
            if len(buffer_array) != 0:
                with open(args.output, 'a') as f:
                    f.writelines(buffer_array)
                del buffer_array
                gc.collect()
                buffer_array = []
            if args.verbose:
                print(f'[*] All temporary resources freed by level {_+2}')
