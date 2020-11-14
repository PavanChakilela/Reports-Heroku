import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import openpyxl

# To Improve speed and cache data
@st.cache(persist=True, allow_output_mutation=True)
def explore_data(dataset):
    df = pd.read_csv(dataset)
    dataset.seek(0)
    return df

#PENDING ???
def project_selector(data):
    projectlist = os.listdir(folder_path)
    selected_projectid = st.selectbox('Select a Project', projectlist)
    return selected_projectid
    
#Map Designations 
def map_designations(proj_data):     
    proj_data.loc[proj_data['Grade Id'] == "E80", 'Designation'] = "PAT"
    proj_data.loc[proj_data['Grade Id'] == "E75", 'Designation'] = "PA"
    proj_data.loc[proj_data['Grade Id'] == "E70", 'Designation'] = "PA"   
    proj_data.loc[proj_data['Grade Id'] == "E65", 'Designation'] = "A"
    proj_data.loc[proj_data['Grade Id'] == "E60", 'Designation'] = "SA"
    proj_data.loc[proj_data['Grade Id'] == "E50", 'Designation'] = "M"        
    proj_data.loc[proj_data['Grade Id'] == "E45", 'Designation'] = "SM"
    proj_data.loc[proj_data['Grade Id'] == "E40", 'Designation'] = "AD"
    proj_data.loc[proj_data['Grade Id'] == "E35", 'Designation'] = "D"
    proj_data.loc[proj_data['Grade Id'] == "E33", 'Designation'] = "SD"  
    return proj_data     
    
#Calculate and Display FTE counts 
def display_FTE_count(proj_data):           
    c1,c2,c3, c4 = st.beta_columns([1.2,1,1,1])
            
    with c1:
        with st.beta_expander("Count of Associates"):
            st.write(len(proj_data))

    with c2:
        with st.beta_expander("Total FTE"):
            st.write(proj_data['Allocation Percentage'].sum()/100.0)

    with c3:
        with st.beta_expander("Onsite FTE"):
            on_filter = (proj_data['Offshore/Onsite'] == 'Onsite')
            st.write(proj_data[on_filter]['Allocation Percentage'].sum()/100.0) 

    with c4:
        with st.beta_expander("Offshore FTE"):
            off_filter = (proj_data['Offshore/Onsite'] == 'Offshore')
            st.write(proj_data[off_filter]['Allocation Percentage'].sum()/100.0)
    return proj_data  

def get_new_labels(sizes, labels):
    new_labels = [label if size > 1 else '' for size, label in zip(sizes, labels)]
    return new_labels
    
def my_autopct(pct):
    return ('%1.1f%%' % pct) if pct > 5 else '' 

#calc percentages of pie 
def cal_pie_percentages(proj_FTE_matrix, location):            
    f1 = (proj_FTE_matrix.loc["PAT",location] + proj_FTE_matrix.loc["PA",location]) / (proj_FTE_matrix.loc["TOTAL",location]) * 100.0
    f2 = (proj_FTE_matrix.loc["A",location]) / (proj_FTE_matrix.loc["TOTAL",location]) * 100.0
    f3 = (proj_FTE_matrix.loc["SA",location]) / (proj_FTE_matrix.loc["TOTAL",location]) * 100.0
    f4 = (proj_FTE_matrix.loc["M",location]) / (proj_FTE_matrix.loc["TOTAL",location]) * 100.0
    f5 = (proj_FTE_matrix.loc["SM",location] + proj_FTE_matrix.loc["AD",location] +\
          proj_FTE_matrix.loc["D",location] + proj_FTE_matrix.loc["SD",location]) / (proj_FTE_matrix.loc["TOTAL",location]) * 100.0
    fracs =  [f1, f2, f3, f4, f5] 
    return fracs

#DataFrame for Project FTE split
    #       Offshore    Onsite  TOTAL
    #PAT
    #PA
    #A
    #SA
    #M
    #SM
    #AD
    #D
    #SD
    #TOTAL
def display_FTE_designation_split(proj_data):    
    proj_FTE_matrix = pd.DataFrame({'Offshore' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Onsite' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \
                                    'TOTAL' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]})
    
    # round to two decimal places in python pandas 
    pd.set_option('precision', 2)   
    
    proj_FTE_matrix['Designation'] = "PAT PA A SA M SM AD D SD TOTAL".split()
    proj_FTE_matrix.set_index('Designation', inplace=True)
    
    designation_list = ["PAT", "PA", "A", "SA", "M", "SM", "AD", "D", "SD", "TOTAL"]
    location_list = ["Offshore", "Onsite"]
    
    #Per each Designation & Location
    for designation in designation_list:
        for location in location_list:
            des_filter = (proj_data['Designation'] == designation) & (proj_data['Offshore/Onsite'] == location)
            proj_FTE_matrix.loc[designation,location] = proj_data[des_filter]['Allocation Percentage'].sum()/100.0
    
    #Total Offshore
    des_filter = (proj_data['Offshore/Onsite'] == 'Offshore')
    proj_FTE_matrix.loc['TOTAL','Offshore'] = proj_data[des_filter]['Allocation Percentage'].sum()/100.0
        
    #Total Onsite    
    des_filter = (proj_data['Offshore/Onsite'] == 'Onsite')
    proj_FTE_matrix.loc['TOTAL','Onsite'] = proj_data[des_filter]['Allocation Percentage'].sum()/100.0

    #Total Column (sum of Offshore & Onsite rows)
    proj_FTE_matrix.loc[:,'TOTAL'] = proj_FTE_matrix.loc[:,'Offshore'] + proj_FTE_matrix.loc[:,'Onsite']
    
    c1,c2 = st.beta_columns([1.5,2])
     
    #Display FTE Designation Matrix View 
    with c1:
        cm = sns.light_palette("green", as_cmap=True) 
        st.dataframe(proj_FTE_matrix.style.background_gradient(cmap=cm))

    with c2:
        labels = 'PA-', 'A', 'SA', 'M', 'SM+'
        f1 = 0
        f2 = 0
        f3 = 0
        f4 = 0 
        f5 = 0
                    
        # Make figure and axes
        fig, axs = plt.subplots(2, 2)          
                    
        # TOTAL pie plot
        if proj_FTE_matrix.loc["TOTAL","TOTAL"] > 0:
            total_fracs = cal_pie_percentages(proj_FTE_matrix, "TOTAL")        
            axs[0, 0].set_title("Overall")    
            patches, texts, autotexts = axs[0, 0].pie(total_fracs, labels=get_new_labels(total_fracs, labels), autopct=my_autopct, textprops={'size': 'smaller'}, \
                                        shadow=True, explode=(0, 0, 0, 0, 0), startangle=90)  
            plt.setp(autotexts, size='x-small')
            autotexts[0].set_color('white')        
        
        # TOTAL On/Off ratio
        if proj_FTE_matrix.loc["TOTAL","TOTAL"] > 0:
            f1 = (proj_FTE_matrix.loc["TOTAL","Onsite"]) / (proj_FTE_matrix.loc["TOTAL","TOTAL"]) * 100.0
            f2 = (proj_FTE_matrix.loc["TOTAL","Offshore"]) / (proj_FTE_matrix.loc["TOTAL","TOTAL"]) * 100.0
            axs[0, 1].set_title("On/Off Ratio")
            axs[0, 1].pie([f1, f2], labels=['On', 'Off'], autopct='%.0f%%', shadow=True, explode=(0, 0), startangle=90)
                      
        #Offshore pie plot   
        if proj_FTE_matrix.loc["TOTAL","Offshore"] > 0:
            off_fracs = cal_pie_percentages(proj_FTE_matrix, "Offshore")
            axs[1, 0].set_title("Offshore")    
            patches, texts, autotexts = axs[1, 0].pie(off_fracs, labels=get_new_labels(off_fracs, labels), autopct=my_autopct, textprops={'size': 'smaller'}, \
                                        shadow=True, explode=(0, 0, 0, 0, 0), startangle=90)  
            plt.setp(autotexts, size='x-small')
            autotexts[0].set_color('white')
        
        #Onsite pie plot   
        if proj_FTE_matrix.loc["TOTAL","Onsite"] > 0:
            on_fracs = cal_pie_percentages(proj_FTE_matrix, "Onsite")
            axs[1, 1].set_title("Onsite")    
            patches, texts, autotexts = axs[1, 1].pie(on_fracs, labels=get_new_labels(on_fracs, labels), autopct=my_autopct, textprops={'size': 'smaller'}, \
                                        shadow=True, explode=(0, 0, 0, 0, 0), startangle=90)  
            plt.setp(autotexts, size='x-small')
            autotexts[0].set_color('white')                                

        st.pyplot(fig) 
    
    return proj_data, proj_FTE_matrix
    
# MultiSelect based on Location / Designation / Department / StartDate / EndDate / AssociateName / Supervisor
def filter_specific_criteria(proj_data, proj2_data):    
    menu_list = st.multiselect("",("Location","Designation","Department","StartDate","EndDate","AssociateName","Supervisor"), key="fil2")
    st.write("You selected",len(menu_list),"fields")
    #print(menu_list, len(menu_list), type(menu_list))
           
    filt_loc = []
    filt_des = []
    filt_dep = []
    filt_name = []
    filt_startdate = []
    filt_enddate = []
    filt_supervisor = []
    for menu_2 in menu_list:
    
        menu_Location = proj2_data['Offshore/Onsite'].unique().tolist()
        menu_Designation = proj2_data['Designation'].unique().tolist()  
        menu_Department = proj2_data['Department Name'].unique().tolist()
        menu_StartDate = proj2_data['Start Date'].unique().tolist()
        menu_EndDate = proj2_data['End Date'].unique().tolist()
        menu_associate_name = proj2_data['Associate Name'].unique().tolist()
        menu_Supervisor = proj2_data['Supervisor Name'].unique().tolist()
        
        if menu_2 == "Location":
            st.subheader("Chose Location")
            filt_loc = st.multiselect("",menu_Location, key="loc")
            
            #Apply Filter
            proj2_filter = (proj2_data['Offshore/Onsite'].isin(filt_loc))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]
                            
        elif menu_2 == "Designation":
            st.subheader("Chose Designation")
            filt_des = st.multiselect("",menu_Designation, key="des")
            
            #Apply Filter
            proj2_filter = (proj2_data['Designation'].isin(filt_des))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]
            
        elif menu_2 == "Department":
            st.subheader("Chose Department")
            filt_dep = st.multiselect("",menu_Department, key="dep")    
            
            #Apply Filter
            proj2_filter = (proj2_data['Department Name'].isin(filt_dep))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]
            
        elif menu_2 == "AssociateName":
            st.subheader("Chose AssociateName")
            filt_name = st.multiselect("",menu_associate_name, key="nam")    
            
            #Apply Filter
            proj2_filter = (proj2_data['Associate Name'].isin(filt_name))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]   

        elif menu_2 == "StartDate":
            st.subheader("Chose StartDate")
            filt_startdate = st.multiselect("",menu_StartDate, key="stdate")    
            
            #Apply Filter
            proj2_filter = (proj2_data['Start Date'].isin(filt_startdate))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]   

        elif menu_2 == "EndDate":
            st.subheader("Chose EndDate")
            filt_enddate = st.multiselect("",menu_EndDate, key="endate")    
            
            #Apply Filter
            proj2_filter = (proj2_data['End Date'].isin(filt_enddate))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]   

        elif menu_2 == "Supervisor":
            st.subheader("Chose Supervisor")
            filt_supervisor = st.multiselect("",menu_Supervisor, key="sup")    
            
            #Apply Filter
            proj2_filter = (proj2_data['Supervisor Name'].isin(filt_supervisor))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]
                     
    #Display Filtered Dataframe
    st.dataframe(proj2_data[['Associate Id', 'Associate Name', 'Designation', 'Project Name', 'Allocation Percentage', 'Offshore/Onsite', 'Department Name', 'Start Date', 'End Date', 'Supervisor Name']], height=200)
    
    return proj_data, proj2_data
    
#compare 2 diff sheets    
def data_diff3(df1, df2):
    comparison_values = df1.eq(df2) 
    #st.dataframe(comparison_values)
    rows,cols=np.where(comparison_values==False)
    print(rows, cols)
    for item in zip(rows,cols):
        df1.iloc[item[0], item[1]] = '{} --> {}'.format(df1.iloc[item[0], item[1]],df2.iloc[item[0], item[1]])
    st.dataframe(df1)  
    df1.to_csv('diff.csv') 

def dataframe_difference(df1, df2, which=None):
    """Find rows which are different."""
    comparison_df = pd.merge(df1, df2, indicator=True, how='outer')
    if which is None:
        diff_df = comparison_df[comparison_df['_merge'] != 'both']
    else:
        diff_df = comparison_df[comparison_df['_merge'] == which]
    return diff_df    
    

#Check if "FTE view of Merged 2 sheets (MBM & BTM)"
def file_upload_2(data1):    
    st.sidebar.warning("Do you want to Merge with 2nd IMIS file?")
    my_dataset2 = st.sidebar.file_uploader("Upload 2nd IMIS Allocation File in CSV format", type=["csv"])
    data3=data1
    if my_dataset2 is not None:
        #Open IMIS file2
        data2 = explore_data(my_dataset2) 
                
        #Append this file2 IMIS contents
        #data3 = data1.append(data2, ignore_index=True, sort=False) 
        data3 = pd.concat([data1, data2], sort=False) 
    return data3  

def pipeline_opp_handling():
    pipe_dataset1 = st.sidebar.file_uploader("Upload Bulk Upload File in CSV format", type=["csv"])
    if pipe_dataset1 is not None:

        #Open PipeLine Opportunity File for Bulk Upload
        pipe_data1 = explore_data(pipe_dataset1)
        
        #Opportunities Specific
        st.subheader("Show Opportunity details")          
                  
        pipe_data1['TCV'] = pipe_data1['Total Deal Value']
        pipe_data1['COGTCV'] = pipe_data1['Cogni Revenue $']
      
        #Display project specific DataFrame for the selected List of Projects
        st.dataframe(pipe_data1)
        
        c1,c2 = st.beta_columns([1,1.25])
    
        #Display Shared vs Small TCV
        with c1:
            # Make figure and axes
            fig, axs = plt.subplots(1,1)
                                                
            shared_filter = (pipe_data1['Segment'] == 'Shared')            
            shared_tcv = pipe_data1[shared_filter]['TCV'].sum()/1000000.0
                       
            small_filter = (pipe_data1['Segment'] == 'Small')            
            small_tcv = pipe_data1[small_filter]['TCV'].sum()/1000000.0
                        
            shared_cogtcv = pipe_data1[shared_filter]['COGTCV'].sum()/1000000.0
            small_cogtcv = pipe_data1[small_filter]['COGTCV'].sum()/1000000.0            
                                    
            xaxis = ["SHC-TCV", "SHC-COG", "SC-TCV", "SC-COG"]
            yaxis = [shared_tcv, shared_cogtcv, small_tcv, small_cogtcv]
            plt.bar(xaxis, yaxis)

            plt.title("(Shared vs Small) vs (Overall Deal vs Cog) in Mil")
            plt.ylabel("in USD mil")
            plt.xlabel("(Shared vs Small) vs (Overall Deal vs Cog)")
            
            for i in range(len(yaxis)):
                plt.annotate(str(yaxis[i]), xy=(i,yaxis[i]), ha='center')
               
            st.pyplot(fig)

        with c2:               
            # Make figure and axes
            #fig, axs = plt.subplots()
            #plt.title("Year vs TCV view (in USD Mil)")
            #plt.ylabel("TCV in USD Mil")
            #plt.xlabel("ConfidenceFactor")
            #                                
            #xaxis = pipe_data1['Confidence Factor %'].unique().tolist()
            #yaxis = []
            #for conf_item in xaxis:  
            #    conf_item_filter = (pipe_data1['Confidence Factor %'] == conf_item)      
            #    yaxis.append(pipe_data1[conf_item_filter]['TCV'].sum()/1000000.0)
            #                 
            #axs.bar(xaxis, yaxis, width = 5)   
            #                    
            #st.pyplot(fig)
            
            # Make figure and axes
            fig, axs = plt.subplots(1,1)
            plt.title("Application vs TCV view (in USD Mil)")
            plt.xlabel("TCV in USD Mil")
            plt.ylabel("Application")
            axs.barh(pipe_data1['Application'], pipe_data1['TCV']/1000000.0 )
               
            st.pyplot(fig)
        
        # Multi Plots
        if st.checkbox("Dynamic Multi Column Plot for TCV vs COGTCV"):
            st.text("Bar Charts By Target/Columns")

            all_columns_names = pipe_data1.columns.tolist()
            all_columns_names.remove('TCV')
            all_columns_names.remove('Total Deal Value')
            all_columns_names.remove('COGTCV')
            all_columns_names.remove('Cogni Revenue $')                
            
            primary_col = st.multiselect('Select Primary Column To Group By',all_columns_names, default="Segment", key="pri")
            selected_column_names = st.multiselect('Select Columns',['TCV', 'COGTCV'], default="TCV", key="sec")
            plot_choice = st.radio("",("Vert Plot", "Hz Plot"))
            st.text("Generating Plot for: {} and {}".format(primary_col,selected_column_names))
            if selected_column_names:
                vc_plot = pipe_data1.groupby(primary_col)[selected_column_names].sum()/1000000.0
                st.write(vc_plot)        
            else:
               vc_plot = pipe_data1.iloc[:,-1].value_counts()
            
            if plot_choice == "Vert Plot":        
                st.write(vc_plot.plot(kind='bar'))
            else:
                st.write(vc_plot.plot(kind='barh'))
                
            if st.button("Download as OppDown1.xlsx to Current Folder"):                    
                writer3 = pd.ExcelWriter('OppDown1.xlsx')
                vc_plot.to_excel(writer3, sheet_name = 'Pipeline-Opp', index = True)
                pipe_data1.to_excel(writer3, sheet_name = 'Original', index = True)
                writer3.save()
                
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
            
    
def main():

    html_temp = """
		<div style="background-color:{};padding:1px;border-radius:2px">
		<h2 style="color:{};text-align:center;">ProjectManager Dashboard </h2>
		</div>
		"""
    st.markdown(html_temp.format('royalblue','white'),unsafe_allow_html=True)
    
    menu = ["Project FTE View", "Compare 2 versions", "Pipeline Opp", "RevRec", "About"]
    choice = st.sidebar.selectbox("Select Option",menu)

    if choice == "Project FTE View":
        
        html_temp2 = """ <h3 style="color:{};text-align:center;">FTE View </h3> """
        st.markdown(html_temp2.format('royalblue','white'),unsafe_allow_html=True)
        
        my_dataset = st.sidebar.file_uploader("Upload IMIS Allocation File in CSV format", type=["csv"])
        
        if my_dataset is not None:

            #Open IMIS file
            data1 = explore_data(my_dataset)
            
            #Default Dataframe
            data = data1
            
            #Check if "FTE view of Merged 2 sheets (MBM & BTM)" & append to DATA
            data = file_upload_2(data1)
            
            #All Projects, All Associates as-is dataframe
            st.subheader("Show ALL Projects Associates")
                
            with st.beta_expander('Complete View (as-is IMIS report)',expanded=False):
                st.dataframe(data)
                
            #Project Specific
            st.subheader("Show Project specific ASSOCIATE details")
            
            #Remove duplicate project-ids
            project_list = data['Project Id'].unique().tolist()

            #selection based on projects list
            project_id_list = st.multiselect("Pls select project(s)", project_list, key="fil1")
            
            #List of projects for which query is needed
            proj_filt1 = data['Project Id'].isin(project_id_list)
            
            #New dataframe of PROJ selected using multiselect
            proj_data = data[proj_filt1]
            
            #Map Designations   
            proj_data = map_designations(proj_data)        
            
            #Display project specific DataFrame for the selected List of Projects
            st.dataframe(proj_data[['Associate Id', 'Associate Name', 'Designation', 'Project Name', \
            'Allocation Percentage', 'Offshore/Onsite', 'Department Name', 'Start Date', 'End Date', 'Supervisor Name']], height=200)
          
            #Calculate and Display FTE TOTAL counts               
            proj_data = display_FTE_count(proj_data)
            
            #DataFrame for Project FTE split
            proj_data, proj_FTE_matrix = display_FTE_designation_split(proj_data)
            
            if st.button("Download as file1.xlsx to Current Folder"):
                #proj_data.to_csv("file1.xlsx")
                
                writer1 = pd.ExcelWriter('file1.xlsx')
                proj_FTE_matrix.to_excel(writer1, sheet_name = 'FTE1-Split', index = True)
                proj_data.to_excel(writer1, sheet_name = 'FTE1', index = True)
                writer1.save()
               
            #MultiSelect based on Location / Designation / Department / StartDate / EndDate / AssociateName / Supervisor
            #New dataframe : PROJ2 before filter same as PROJ
            proj2_data = proj_data
            if st.checkbox("Filter based on Location, Designation, Department, StartDate, EndDate, AssociateName, Supervisor"): 
                proj_data, proj2_data = filter_specific_criteria(proj_data, proj2_data)
                
                proj2_data, proj_FTE_matrix = display_FTE_designation_split(proj2_data)
                
                if st.button("Download as file2.xlsx to Current Folder"):
                    #proj2_data.to_csv("file2.csv")
                                        
                    writer2 = pd.ExcelWriter('file2.xlsx')
                    proj_FTE_matrix.to_excel(writer2, sheet_name = 'FTE2-Split', index = True)
                    proj2_data.to_excel(writer2, sheet_name = 'FTE2', index = True)
                    writer2.save()
 
    elif choice == "Compare 2 versions":
        
        my_dataset1 = st.sidebar.file_uploader("Upload 1st IMIS Allocation File in CSV format", type=["csv"])
        if my_dataset1 is not None:

            #Open IMIS file1
            data1 = explore_data(my_dataset1)

        my_dataset2 = st.sidebar.file_uploader("Upload 2nd IMIS Allocation File in CSV format", type=["csv"])
        if my_dataset2 is not None:

            #Open IMIS file2
            data2 = explore_data(my_dataset2)        
        
            #Compare 2 versions
            st.subheader("Comparision of 2 versions")
                
            with st.beta_expander('Complete View (as-is IMIS report1)',expanded=False):
                st.dataframe(data1)
            
            with st.beta_expander('Complete View (as-is IMIS report2)',expanded=False):
                st.dataframe(data2)            
                
            #Project Specific
            st.subheader("Comparision Report -- PENDING DB ???")
            
            #Compare - PENDING ???
            #diff_df = dataframe_difference(data1, data2)
            #if st.button("Download as diff.csv to Current Folder"):
            #    diff_df.to_csv('diff.csv')    

    elif choice == "Pipeline Opp":
    
        html_temp2 = """ <h3 style="color:{};text-align:center;">PipeLine Opportunity View </h3> """
        st.markdown(html_temp2.format('royalblue','white'),unsafe_allow_html=True)
        
        pipeline_opp_handling()        
            
                  
if __name__ == '__main__':
    main()