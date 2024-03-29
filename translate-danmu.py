import polars as pl
import os
from googletrans import Translator
translator = Translator()
import numpy as np

# def translate_text(text):
    
path = '/Users/ischneid/bilibili-comment-translator/comments_and_danmu_orig/Danmu_Muz_translated_lyrics.csv'

df_orig = pl.read_csv(path, truncate_ragged_lines= True)

file_title = path.split("/")[-1][:-4]
target_path = f'/Users/ischneid/bilibili-comment-translator/comments_and_danmu_trans/{file_title}.csv'

df_orig = df_orig[1: , 0:5]
df_orig.cast({'/i': pl.Int64})

print(df_orig)

final_df_schema = {
    "id": pl.Int64,
    "column_2": str,
    "column_3": str,
    "time_stamps": str,
    "comment_text_chinese": str,
    "comment_text_english": str}

try:
   final_df = pl.read_csv(target_path)

   print(final_df)

except FileNotFoundError:
    final_df = pl.DataFrame(schema = final_df_schema)
    final_df.write_csv(target_path)

    # print(final_df)
    
def translate_comments():

    # df_orig = df_orig[0:20]

    index_list_orig = (len(df_orig))
    index_orig = list(range(index_list_orig))

    index_list_final = (len(final_df))
    index_final = list(range(index_list_final))

    matrix_orig = np.array(index_orig, dtype = int)

    if len(index_final) > 0:
        matrix_final = np.array(index_final, dtype = int)
        matrix_final = np.pad(index_final, (0, len(matrix_orig) - len(matrix_final)))
    else:
        matrix_final = np.zeros(len(index_orig), dtype=int)
    
    # print(matrix_final)

        # print(matrix_orig)
        # print(matrix_final)

        # Find the maximum length of the two lists
        max_length = max(len(index_orig), len(index_final))

        # Pad the smaller list with zeroes to match the maximum length
        # matrix_orig = np.pad(index_orig, (0, max_length - len(index_orig)))
        matrix_final = np.pad(index_final, (0, max_length - len(index_final)))

        print(matrix_orig)
        print(matrix_final)

    unique_index = np.array(matrix_orig - matrix_final, dtype=int).tolist()

    unique_index = [i for i in unique_index if i != 0]

    # print(df_orig[4])

    if len(unique_index) == 0:
        print("I'm done!")
        quit()

    else:
        print(f'I have {len(unique_index)} comments left to translate.')

    for i in unique_index:

        try:

            # print(df_orig[i])

            text_to_translate = str(df_orig[i, 4])
            english_text = translator.translate(text_to_translate).text
            # print(english_text)

            # print((english_text))

            data = {
                "id": df_orig[i, 0],
                "column_2": df_orig[i, 1],
                "column_3": df_orig[i, 2],
                "time_stamps": df_orig[i, 3],
                "comment_text_chinese": df_orig[i, 4],
                "comment_text_english": english_text}
                
            
            # print(data)

            df = pl.DataFrame(data, schema = final_df_schema)
            # print(df)
            # quit()

            # print(df)

            final_df.extend(df)
            final_df.write_csv(target_path)

        except (TimeoutError):
            print("Time to start over.")
        #     # quit()
            translate_comments()
        except Exception as e:
            print(f'An error occured: {e}. I will start again.')
            # quit()
            translate_comments()
    print("I'm done!")
    return
        
translate_comments()
