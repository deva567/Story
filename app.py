import streamlit as st
import pandas as pd
import numpy as np

class Lyrics:
    def __init__(self):
        self.final_dict={}
        
    def generator(self,data,split):
    
        for i in range(len(data)-split):
            x=data[i:i+split]
            y=data[i+split]
            if self.final_dict.get(x) is None:
                self.final_dict[x]={}
                self.final_dict[x][y]=1
            else:
                if self.final_dict[x].get(y) is None:
                    self.final_dict[x][y]=1
                else:
                    self.final_dict[x][y]+=1
        return True
    
    
    def future_data(self,startString,val,split):

        for i in range(val):
            inp = startString[-split:]

            possible_chars = list(self.final_dict[inp].keys())
            possible_values = list(self.final_dict[inp].values())

            sum_ = sum(self.final_dict[inp].values())

            probabs =  np.array(possible_values)/sum_

            next_char = np.random.choice(possible_chars, p = probabs)

            startString += next_char
        return startString
        


def main():
    """Semi Automated ML App with Streamlit """
    activities = ["EDA","Plots"]	
    choice = st.sidebar.selectbox("Select Activities",activities)

    if choice == 'EDA':
        result = st.file_uploader("Upload", type="txt")

        # filename =st.text_input('Enter a file path:')
        try:
            if result:
        # Process you file here
                data = result.getvalue()
                # file1 = open(filename,"r") 
                # data=file1.read()
                data=data.lower().replace('\n','')
                # file1.close() 
                st.write(data[:200])
                obj=Lyrics()
                add_split = st.sidebar.slider(
                    'Select a split of values',
                    2, 25
                )
                st.write("Select Split from Left Slider .")
                if add_split>3:
                # split=st.text_input("Enter String split for Prediction :")
                    gen=obj.generator(data=data,split=int(add_split))
                    if gen:
                        startString=st.text_input("Enter Starting String for Prediction :")
                        if len(startString)>0:
                            val=st.sidebar.slider(
                            "How many char's want's to Prediction :",
                            100, 1000
                            )
                            st.write("Select no of  char's want's to Prediction from Left Slider .")
                            if val>100:
                                final_op=obj.future_data(startString,val,add_split)
                                st.write(final_op)
        except FileNotFoundError:
            st.error('File not found.')
        except IndexError:
            st.error('Select only one Author. ')
        except KeyError:
            st.error("Enter correct Integer. ")

        


if __name__ == '__main__':
	main()
