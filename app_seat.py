from pathlib import Path
import sqlite3
from sqlite3 import Connection
import streamlit as st
import pandas as pd

# FileUpload Related Functions
from app import *

#Seat Config Details
import seat_config

URI_SQLITE_DB = "seat1.db"

#Duplicate of --> map_designations but handles Grade instead of Grade_Id
def seat_map_designations(proj_data):     
    pd.options.mode.chained_assignment = None  # default='warn'
    proj_data.loc[proj_data.loc[:, 'Grade'] == 80, 'Designation'] = "PAT"
    proj_data.loc[proj_data.loc[:, 'Grade'] == 82, 'Designation'] = "PAT"     #Analyst Trainee considered as PAT
    proj_data.loc[proj_data.loc[:, 'Grade'] == 85, 'Designation'] = "PAT"     #Programmer Trainee considered as PAT
    proj_data.loc[proj_data.loc[:, 'Grade'] == 90, 'Designation'] = "PAT"
    proj_data.loc[proj_data.loc[:, 'Grade'] == 75, 'Designation'] = "PA"      #Programmer considered as PA
    proj_data.loc[proj_data.loc[:, 'Grade'] == 70, 'Designation'] = "PA"   
    proj_data.loc[proj_data.loc[:, 'Grade'] == 65, 'Designation'] = "A"    
    proj_data.loc[proj_data.loc[:, 'Grade'] == 60, 'Designation'] = "SA"   
    proj_data.loc[proj_data.loc[:, 'Grade'] == 50, 'Designation'] = "M"
    proj_data.loc[proj_data.loc[:, 'Grade'] == 45, 'Designation'] = "SM"
    proj_data.loc[proj_data.loc[:, 'Grade'] == 40, 'Designation'] = "AD"
    proj_data.loc[proj_data.loc[:, 'Grade'] == 35, 'Designation'] = "D"
    proj_data.loc[proj_data.loc[:, 'Grade'] == 33, 'Designation'] = "SD"
    proj_data.loc[proj_data.loc[:, 'Grade'] == 30, 'Designation'] = "SD"      #SBU Head - Practice considered as SD
    proj_data.loc[proj_data.loc[:, 'Grade'] == 25, 'Designation'] = "SD"      #SBU Head - MDU considered as SD
    proj_data.loc[proj_data.loc[:, 'Grade'] == 20, 'Designation'] = "SD"      #SBU Leader - INS considered as SD
    return proj_data 

def dataframe_statistics(seat_df, seat2_df):
        st.info("Check ALL possible values ***to give you an idea ! ***")
        cm = sns.light_palette("green", as_cmap=True)
        c1, c2 = st.beta_columns([1,1.2])
        
        with c1:
            LOB_list = seat2_df['LOB'].unique().tolist()
            with st.beta_expander(f'List of LOBs ({len(LOB_list)})',expanded=False):
                st.dataframe(pd.DataFrame(seat2_df['LOB'].value_counts(dropna=False)).style.background_gradient(cmap=cm))  
                #List of LOBs
                #st.write(LOB_list) 
        
        with c2:
            Service_Grouping_list = seat2_df['Service_Grouping'].unique().tolist()
            with st.beta_expander(f'Service_Grouping ({len(Service_Grouping_list)})',expanded=False):
                st.dataframe(pd.DataFrame(seat2_df['Service_Grouping'].value_counts(dropna=False)).style.background_gradient(cmap=cm))                   
        
        c1, c2 = st.beta_columns([1,1.2])        
        with c1:
            Include_Exclude_list = seat2_df['Include_Exclude'].unique().tolist()
            with st.beta_expander(f'Include_Exclude ({len(Include_Exclude_list)})',expanded=False):
                st.dataframe(pd.DataFrame(seat2_df['Include_Exclude'].value_counts(dropna=False)).style.background_gradient(cmap=cm))    
                
        with c2:
            Account_Name_list = seat2_df['Account_Name'].unique().tolist()
            with st.beta_expander(f'Account_Names ({len(Account_Name_list)})',expanded=False):
                st.dataframe(pd.DataFrame(seat2_df['Account_Name'].value_counts(dropna=False)).style.background_gradient(cmap=cm))        
       
        #c1, c2 = st.beta_columns([1,1.2])
        #with c1:
        Project_Description_list = seat2_df['Project_Description'].unique().tolist()
        with st.beta_expander(f'List of Projects ({len(Project_Description_list)})',expanded=False): 
            st.dataframe(pd.DataFrame(seat2_df['Project_Description'].value_counts(dropna=False)).style.background_gradient(cmap=cm)) 
                                        
        #with c2:
        Department_Name_list = seat2_df['Department_Name'].unique().tolist()
        with st.beta_expander(f'Department_Names ({len(Department_Name_list)})',expanded=False):
            st.dataframe(pd.DataFrame(seat2_df['Department_Name'].value_counts(dropna=False)).style.background_gradient(cmap=cm))
                
        c1, c2, c3 = st.beta_columns([1,1,2])        
        with c1:
            Country_list = seat2_df['Country'].unique().tolist()
            with st.beta_expander(f'Country ({len(Country_list)})',expanded=False):
                st.dataframe(pd.DataFrame(seat2_df['Country'].value_counts(dropna=False)).style.background_gradient(cmap=cm)) 
                
        with c2:
            City_list = seat2_df['City'].unique().tolist()
            with st.beta_expander(f'City ({len(City_list)})',expanded=False):
                st.dataframe(pd.DataFrame(seat2_df['City'].value_counts(dropna=False)).style.background_gradient(cmap=cm)) 
                
        with c3:    
            Revised_Location_list = seat2_df['Revised_Location'].unique().tolist()
            with st.beta_expander(f'Revised_Location ({len(Revised_Location_list)})',expanded=False):
                st.dataframe(pd.DataFrame(seat2_df['Revised_Location'].value_counts(dropna=False)).style.background_gradient(cmap=cm)) 
                
        c1, c2 = st.beta_columns([1,1])        
        with c1:
            Shared_Dedicated_Seat_list = seat2_df['Shared_Dedicated_Seat'].unique().tolist()
            with st.beta_expander(f'Shared_Dedicated_Type ({len(Shared_Dedicated_Seat_list)})',expanded=False):
                st.dataframe(pd.DataFrame(seat2_df['Shared_Dedicated_Seat'].value_counts(dropna=False)).style.background_gradient(cmap=cm))
        with c2:
            Proposed_Seat_Details_list = seat2_df['Proposed_Seat_Details'].unique().tolist()
            with st.beta_expander(f'Proposed_Seat_Details ({len(Proposed_Seat_Details_list)})',expanded=False):
                st.dataframe(pd.DataFrame(seat2_df['Proposed_Seat_Details'].value_counts(dropna=False)).style.background_gradient(cmap=cm))    

        Seat_Type_Associate_list = seat2_df['Seat_Type_Associate'].unique().tolist()
        with st.beta_expander(f'Associate_Details with Seat ({len(Seat_Type_Associate_list)})',expanded=False): 
            #st.write(Seat_Type_Associate_list)
            st.dataframe(pd.DataFrame(seat2_df['Seat_Type_Associate'].value_counts(dropna=False)).style.background_gradient(cmap=cm))                
            
        #enable download as hyperlink
        st.markdown(get_table_download_link(seat2_df, seat_df, 'Seat-Filter', 'Total-Seats', 'Seat-view'), unsafe_allow_html=True)    


# MultiSelect based on LOB / Service_Grouping / Include_Exclude / Project_Description / Project_Manager_Name / Account_Name 
#                      / Department_Name / City / Revised_Location / Floor_Wing_Module / Shared_Dedicated_Seat / Cubicle_Type / Required_Cog_Laptop
def filter_seat_criteria(seat_df, seat2_df):    
    menu_list = st.multiselect("",("LOB", "Service_Grouping", "Include_Exclude", "Project_Description", "Project_Manager_Name", "Account_Name",\
                                   "Department_Name", "City", "Revised_Location", "Floor_Wing_Module", "Shared_Dedicated_Seat", "Cubicle_Type", \
                                   "Required_Cog_Laptop", \
                                   "Proposed_Seat_Details", "Seat_Type_Associate", \
                                   "Freq_Proposed_Seat_Details"), key="seatfil2")
    st.write("You selected",len(menu_list),"fields")
                   
    for menu_2 in menu_list:    

        menu_2_list = seat2_df[menu_2].unique().tolist()

        st.subheader(f"Chose ({menu_2})")

        filt_seat_df = st.multiselect("",menu_2_list, key="loc")
            
        #Apply Filter
        seat2_filter = (seat2_df[menu_2].isin(filt_seat_df))

        #New filtered PROJ2
        seat2_df = seat2_df[seat2_filter]
                                                 
    #Display Filtered Dataframe
    st.dataframe(seat2_df, height=200)
    
    return seat_df, seat2_df

#input: seat_df (original)
#output: seat_err_df (error DF), seat_filter_df (Filtered DF post Errors of seat_err_df) 
def seat_df_error_scenario(seat_df):

    #Seat_df (original) whereas seat_filter_df is filtered DF 
    seat_filter_df = seat_df.copy()

    #RFP scope but Excluded
    RFP_filter = ((seat_filter_df['Service_Grouping'] == 'Invest & Maintenance') & (seat_filter_df['Include_Exclude'] == 'Exclude'))  
    seat_err_df2 = seat_filter_df[RFP_filter]
    seat_err_df2['ErrorScenario'] = "RFP Scoped but Excluded"
    seat_err_df = seat_err_df2
    seat_filter_df['ErrorScenario'] = np.where(RFP_filter, "RFP Scoped but Excluded", "NoError")
    NonError_filter = (seat_filter_df['ErrorScenario'] == "NoError")
    seat_filter_df = seat_filter_df[NonError_filter]
    
              
    #Not-RFP scope, but Included
    MPS_filter = ((seat_filter_df['Service_Grouping'] == 'Production Support') & (seat_filter_df['Include_Exclude'] == 'Include'))  
    seat_err_df2 = seat_filter_df[MPS_filter]
    seat_err_df2['ErrorScenario'] = "RFP Not-scoped but Included"
    seat_err_df = pd.concat([seat_err_df, seat_err_df2], sort=False, ignore_index=False) 
    seat_filter_df['ErrorScenario'] = np.where(MPS_filter, "RFP Not-scoped but Included", "NoError")
    NonError_filter = (seat_filter_df['ErrorScenario'] == "NoError")
    seat_filter_df = seat_filter_df[NonError_filter] 
    #st.dataframe(seat_df)    
            
    #Dedicated but multiple seats tagged
    dedicated_filter = ((seat_filter_df['Shared_Dedicated_Seat'] == 'Dedicated') & (seat_filter_df['Freq_Proposed_Seat_Details'] > 1))  
    seat_err_df2 = seat_filter_df[dedicated_filter]
    seat_err_df2['ErrorScenario'] = "Dedicated but MoreThan-1-Seat-Tagged"
    seat_err_df = pd.concat([seat_err_df, seat_err_df2], sort=False, ignore_index=False) 
    seat_filter_df['ErrorScenario'] = np.where(dedicated_filter, "Dedicated but MoreThan-1-Seat-Tagged", "NoError")
    NonError_filter = (seat_filter_df['ErrorScenario'] == "NoError")
    seat_filter_df = seat_filter_df[NonError_filter]      

    #Shared but  not 2 seats tagged
    shared_filter = ((seat_filter_df['Shared_Dedicated_Seat'] == 'Shared') & (seat_filter_df['Freq_Proposed_Seat_Details'] != 2))  
    seat_err_df2 = seat_filter_df[shared_filter]
    seat_err_df2['ErrorScenario'] = "Shared but 2-Seats-Not-Tagged"
    seat_err_df = pd.concat([seat_err_df, seat_err_df2], sort=False, ignore_index=False)
    seat_filter_df['ErrorScenario'] = np.where(shared_filter, "Shared but 2-Seats-Not-Tagged", "NoError")
    NonError_filter = (seat_filter_df['ErrorScenario'] == "NoError")
    seat_filter_df = seat_filter_df[NonError_filter]    
    
    #City is Hyderabad but NO proper ODC of Hyd tagged
    City_filter = ((seat_filter_df['City'] == 'Hyderabad') & (seat_filter_df['Revised_Location'].isin(['HYD - MDH - SEZ'])== False))  
    seat_err_df2 = seat_filter_df[City_filter]
    seat_err_df2['ErrorScenario'] = "City is Hyderabad but Revised Location is NOT HYD - MDH - SEZ"
    seat_err_df = pd.concat([seat_err_df, seat_err_df2], sort=False, ignore_index=False)
    seat_filter_df['ErrorScenario'] = np.where(City_filter, "City is Hyderabad but Revised Location is NOT HYD - MDH - SEZ", "NoError")
    NonError_filter = (seat_filter_df['ErrorScenario'] == "NoError")
    seat_filter_df = seat_filter_df[NonError_filter]      
    
    #Floor/Wing/Module is Not correct
    Module_filter = ((seat_filter_df['Floor_Wing_Module'].isin(['0', "#N/A", "N/A", "", "n/a", "#n/a", '0Floor-0Wing-0ODC'])))  
    seat_err_df2 = seat_filter_df[Module_filter]
    seat_err_df2['ErrorScenario'] = "Floor/Wing/Module is Blank or N/A"
    seat_err_df = pd.concat([seat_err_df, seat_err_df2], sort=False, ignore_index=False)
    seat_filter_df['ErrorScenario'] = np.where(Module_filter, "Floor/Wing/Module is Blank or N/A", "NoError")
    NonError_filter = (seat_filter_df['ErrorScenario'] == "NoError")
    seat_filter_df = seat_filter_df[NonError_filter]    
    
    return seat_err_df, seat_filter_df

#DataFrame for ODC Metrics
    #                               Loc1    Loc2  TOTAL
    #Overall-Capacity 
    #Total-Dedicated-SeatTagged
    #Total-Shared-SeatTagged
    #Total-Vacant-Seat
    #Total-Planned-RampUp
    #Total-Digital-Lock
    #Total-Seats-ToBeReleased
#@st.cache(persist=False, allow_output_mutation=False, suppress_st_warning=True)
def display_ODC_Metrics(seat_inv_df, key):    

    seat_metrics_df = pd.DataFrame()                                
    
    # round to two decimal places in python pandas 
    pd.set_option('precision', 2) 
    
    #Assuming Inventory is Correct & Final
    #st.write(seat_inv_df['Shared_Dedicated_Seat'].value_counts(dropna=False))
    
    c1, c2 = st.beta_columns([2.8,1])
    
    #Display FTE Designation Matrix View 
    with c1:
        cm = sns.light_palette("green", as_cmap=True) 
        ODC = seat_inv_df['City'][0] + " : " + seat_inv_df['Floor_Wing_Module'][0]
        #st.write(ODC)
        
        seat_metrics_df.loc['Overall-Capacity',ODC] = len(seat_inv_df.index)        
        
        # Get a bool series representing which row satisfies the condition i.e. True for
        seriesObj = seat_inv_df.apply(lambda x: True if x['Shared_Dedicated_Seat'] == 'Dedicated' else False , axis=1)
        # Count number of True in series
        numOfDedicated = len(seriesObj[seriesObj == True].index)
        seat_metrics_df.loc['Total-Dedicated-SeatTagged',ODC] = numOfDedicated 
        
        #Shared Seat Count
        seriesObj = seat_inv_df.apply(lambda x: True if x['Shared_Dedicated_Seat'] == 'Shared' else False , axis=1)       
        numOfShared = len(seriesObj[seriesObj == True].index)        
        seat_metrics_df.loc['Total-Shared-SeatTagged',ODC] = numOfShared
            
        #Vacant Seat Count
        seriesObj = seat_inv_df.apply(lambda x: True if x['Shared_Dedicated_Seat'] == 'Vacant' else False , axis=1)
        numOfVacant = len(seriesObj[seriesObj == True].index)
        seat_metrics_df.loc['Total-Vacant-Seat',ODC] = numOfVacant
                  
    with c2:
        #st.write("Forecast/Digital Lock?")
        numOfForecast = int(st.number_input("Do you have Seats Forecast?",0,20,value=0, step=1, key=key+"fore1"))  
        numOfDigitalLock = int(st.number_input("Do you have Digital Locked Seats?",0,20,value=0, step=1, key=key+"digi1")) 

        #Planned-RampUp / Forecast
        seat_metrics_df.loc['Total-Forecast-RampUp',ODC] = numOfForecast    

        #Digital Lock
        seat_metrics_df.loc['Total-Digital-Lock',ODC] = numOfDigitalLock 

        #Digital Lock
        seat_metrics_df.loc['Total-Seats-ToBeReleased',ODC] = len(seat_inv_df.index) - (numOfDedicated + numOfShared + numOfForecast + numOfDigitalLock)         

    with c1:
        cm = sns.light_palette("green", as_cmap=True)        
        st.dataframe(seat_metrics_df.style.background_gradient(cmap=cm))    

    return seat_metrics_df    
    #st.write(seat_df1['Freq_Proposed_Seat_Details'] = seat_inv_df.groupby('Proposed_Seat_Details')['Proposed_Seat_Details'].transform('count')

def build_seat_inventory(City, Revised_Location, ODC, seat_df, seat_ODC_df, seat_inv_df):

    #for now assumed Revised Location assumed --> HYD - MDH - SEZ
    
    seat_inv = pd.DataFrame.from_dict(seat_config.Hyd_MDH_seat_inv)         
    #st.dataframe(seat_inv)
    
    #st.write(seat_inv['2Floor-AWing-8ODC'][0][2:20:2]) #working fine    
    #    if ODC == '2Floor-AWing-8ODC':
    #        st.write(seat_inv['2Floor-AWing-8ODC'][0][1:6])
    #st.write(seat_inv['2Floor-AWing-7ODC'][0][:])
    #st.write(seat_inv['8Floor-AWing-3ODC'][0][:])
    #st.write("Build Inventory")
    #st.write(City, ODC)
    
    seat_list = seat_inv[ODC][0][:]
    
    #st.write(seat_list)
    #st.dataframe(seat_df)

    #process for each seat in Inventory configured..
    for seat in seat_list:     
    
        #Filter Uploaded file Seat DataFrame per each Seat of Inventory
        Proposed_Seat_Details_filter = ((seat_df['Proposed_Seat_Details'] == seat))  
        
        each_seat_data_df = seat_df[Proposed_Seat_Details_filter]
                    
        #st.write(seat, each_seat_data_df )
           
        seat_records = each_seat_data_df.to_dict(orient ='records')
        #st.write("Count of Seats Tagged / Proposed: ", len(seat_records))
        
        if len(seat_records) == 0:
            #seat is not tagged Empty
            
            new_seat = {'City'                      : City, \
                        'Floor_Wing_Module'         : ODC, \
                        'Seat_Num'                  : seat, \
                        'Shared_Dedicated_Seat'     : "Vacant", \
                        'Cubicle_Type'              : seat[-4], \
                        'Associate_ID1'             : "", \
                        'Associate_Name1'           : "", \
                        'Assest_ID1'                : "", \
                        'Designation1'              : "", \
                        'LOB1'                      : "", \
                        'Project_Description1'      : "", \
                        'Project_Manager_Name1'     : "", \
                        'Department_Name1'          : "", \
                        'Associate_ID2'             : "", \
                        'Associate_Name2'           : "", \
                        'Assest_ID2'                : "", \
                        'Designation2'              : "", \
                        'LOB2'                      : "", \
                        'Project_Description2'      : "", \
                        'Project_Manager_Name2'     : "", \
                        'Department_Name2'          : "", \
                        'Seat_Tagging_Associte_Count' : 0  }
        elif len(seat_records) == 1:           
            new_seat = {'City'                          : City, \
                        'Floor_Wing_Module'             : ODC, \
                        'Seat_Num'                      : seat_records[0].get('Proposed_Seat_Details'), \
                        'Shared_Dedicated_Seat'         : seat_records[0].get('Shared_Dedicated_Seat'), \
                        'Cubicle_Type'                  : seat_records[0].get('Cubicle_Type'), \
                        'Associate_ID1'                 : seat_records[0].get('Associate_ID'), \
                        'Associate_Name1'               : seat_records[0].get('Associate_Name'), \
                        'Assest_ID1'                    : seat_records[0].get('Assest_ID'), \
                        'Designation1'                  : seat_records[0].get('Designation'), \
                        'LOB1'                          : seat_records[0].get('LOB'), \
                        'Project_Description1'          : seat_records[0].get('Project_Description'), \
                        'Project_Manager_Name1'         : seat_records[0].get('Project_Manager_Name'), \
                        'Department_Name1'              : seat_records[0].get('Department_Name'), \
                        'Associate_ID2'                 : "", \
                        'Associate_Name2'               : "", \
                        'Assest_ID2'                    : "", \
                        'Designation2'                  : "", \
                        'LOB2'                          : "", \
                        'Project_Description2'          : "", \
                        'Project_Manager_Name2'         : "", \
                        'Department_Name2'              : "", \
                        'Seat_Tagging_Associte_Count'   : seat_records[0].get('Freq_Proposed_Seat_Details') }        
        elif len(seat_records) == 2:           
            new_seat = {'City'                          : City, \
                        'Floor_Wing_Module'             : ODC, \
                        'Seat_Num'                      : seat_records[0].get('Proposed_Seat_Details'), \
                        'Shared_Dedicated_Seat'         : seat_records[0].get('Shared_Dedicated_Seat'), \
                        'Cubicle_Type'                  : seat_records[0].get('Cubicle_Type'), \
                        'Associate_ID1'                 : seat_records[0].get('Associate_ID'), \
                        'Associate_Name1'               : seat_records[0].get('Associate_Name'), \
                        'Assest_ID1'                    : seat_records[0].get('Assest_ID'), \
                        'Designation1'                  : seat_records[0].get('Designation'), \
                        'LOB1'                          : seat_records[0].get('LOB'), \
                        'Project_Description1'          : seat_records[0].get('Project_Description'), \
                        'Project_Manager_Name1'         : seat_records[0].get('Project_Manager_Name'), \
                        'Department_Name1'              : seat_records[0].get('Department_Name'), \
                        'Associate_ID2'                 : seat_records[1].get('Associate_ID'), \
                        'Associate_Name2'               : seat_records[1].get('Associate_Name'), \
                        'Assest_ID2'                    : seat_records[1].get('Assest_ID'), \
                        'Designation2'                  : seat_records[1].get('Designation'), \
                        'LOB2'                          : seat_records[1].get('LOB'), \
                        'Project_Description2'          : seat_records[1].get('Project_Description'), \
                        'Project_Manager_Name2'         : seat_records[1].get('Project_Manager_Name'), \
                        'Department_Name2'              : seat_records[1].get('Department_Name'),
                        'Seat_Tagging_Associte_Count'   : seat_records[1].get('Freq_Proposed_Seat_Details') }       
                    
        #st.write(seat_records[0].get('Associate_ID'), seat_records[1].get('Associate_ID'))

        seat_inv_df = seat_inv_df.append(new_seat, ignore_index = True)
        seat_ODC_df = seat_ODC_df.append(new_seat, ignore_index = True)
        
    return seat_inv_df, seat_ODC_df         

def seat_utilization(seat_df, seat_filter_df):
        seat_inv_col_names = ['City', 'Floor_Wing_Module', 'Seat_Num', 'Shared_Dedicated_Seat', 'Cubicle_Type', \
                              'Associate_ID1', 'Associate_Name1', 'Assest_ID1', 'Designation1', 'LOB1', 'Project_Description1', 'Project_Manager_Name1', 'Department_Name1', \
                              'Associate_ID2', 'Associate_Name2', 'Assest_ID2', 'Designation2', 'LOB2', 'Project_Description2', 'Project_Manager_Name2', 'Department_Name2', \
                              'Seat_Tagging_Associte_Count']   
        
        #Copy to revised DF 
        seat_inv_df =  pd.DataFrame(columns=seat_inv_col_names)
        seat_inv_df.set_index('Seat_Num', inplace=True)        
  
        #Ignore/Filter all Error Scenarios Rows
        Error_filter = (seat_filter_df['ErrorScenario'] == "NoError")
        #New filtered seat_city_df
        seat_filter_df = seat_filter_df[Error_filter]  
        #st.write(seat_filter_df)
        
        #Overall Seat Metrics DF for Consolidated of all ODCs
        seat_metrics_cons_df = pd.DataFrame()
        
        # for each city & ODC combination from Revised_Location
        City_list = seat_filter_df['City'].unique().tolist()
        City_list = ['Hyderabad']
        for City in City_list:
        
            #Apply City Filter
            City_filter = (seat_filter_df['City'] == City)
            #New filtered DF
            seat_filter_df = seat_filter_df[City_filter]  
            #st.write(City, seat_filter_df)
            
            #Get all Locations of City
            Revised_Location_list = seat_filter_df['Revised_Location'].unique().tolist()
            #for now consider only Revised Location HYD - MDH - SEZ ???
            Revised_Location_list = ["HYD - MDH - SEZ"]
            
            for RevisedLoc in Revised_Location_list:
                RevisedLoc_filter = (seat_filter_df['Revised_Location'] == RevisedLoc)

                #New filtered DF
                seat_filter_df = seat_filter_df[RevisedLoc_filter]
                             
                #Apply ODC Filter
                ODC_list = seat_filter_df['Floor_Wing_Module'].unique().tolist()
                #ODC_list = ['2Floor-AWing-8ODC', '2Floor-AWing-7ODC', '8Floor-AWing-3ODC']

                for ODC in ODC_list:
                    #New filtered ODC specific List
                    ODC_filter = (seat_filter_df['Floor_Wing_Module'] == ODC)
                    seat_filter_df = seat_filter_df[ODC_filter]                    
                            
                    # seat_ODC_df --> ODC seat tagged info
                    # seat_inv_df --> Complete Seat Inventory
                    # seat_df     --> Original Seat DF
                    seat_ODC_df = pd.DataFrame(columns=seat_inv_col_names)        
                    seat_inv_df, seat_ODC_df = build_seat_inventory(City, RevisedLoc, ODC, seat_df, seat_ODC_df, seat_inv_df)
                    
                    #re-order the columns
                    seat_inv_final_df = seat_ODC_df[['City', 'Floor_Wing_Module', 'Seat_Num','Shared_Dedicated_Seat','Seat_Tagging_Associte_Count', 'Cubicle_Type', \
                                             'Associate_ID1', 'Associate_Name1', 'Assest_ID1', 'Designation1', 'LOB1', 'Project_Manager_Name1', 'Department_Name1', \
                                             'Associate_ID2', 'Associate_Name2', 'Assest_ID2', 'Designation2', 'LOB2', 'Project_Manager_Name2', 'Department_Name2' ]]
                    
                    with st.beta_expander(f"{City}, {RevisedLoc}, {ODC}",expanded=False):
                        st.write(seat_inv_final_df)
                        
                        #enable download as hyperlink
                        st.markdown(get_table_download_link(seat_ODC_df, seat_df, 'Seat_ODC_Details', 'Total-Seats', f'Seat-{City}-{ODC}'), unsafe_allow_html=True)  
                                                
                        seat_metrics_df = display_ODC_Metrics(seat_inv_final_df, key=ODC) 
                        #st.write(f"Metrics of {City}, {RevisedLoc}, {ODC}") 
                        seat_metrics_cons_df = pd.concat([seat_metrics_cons_df, seat_metrics_df], axis = 1)
                        #st.dataframe(seat_metrics_cons_df)
         
        with st.beta_expander(f"Overall-{City}",expanded=False):
            seat_inv_final_df = seat_inv_df[['City', 'Floor_Wing_Module', 'Seat_Num','Shared_Dedicated_Seat','Seat_Tagging_Associte_Count', 'Cubicle_Type', \
                                             'Associate_ID1', 'Associate_Name1', 'Assest_ID1', 'Designation1', 'LOB1', 'Project_Manager_Name1', 'Department_Name1', \
                                             'Associate_ID2', 'Associate_Name2', 'Assest_ID2', 'Designation2', 'LOB2', 'Project_Manager_Name2', 'Department_Name2' ]]        
            st.write(seat_inv_final_df)
                    
            #seat_metrics_df = display_ODC_Metrics(seat_inv_final_df, key=City)
            #st.write(f"Metrics of Overall-{City}") 
            #st.dataframe(seat_metrics_df)
            
            seat_metrics_cons_df.insert (loc=0, column="Overall", value=seat_metrics_cons_df.sum(axis=1))
            
            cm = sns.light_palette("green", as_cmap=True)
            st.dataframe(seat_metrics_cons_df.style.background_gradient(cmap=cm))
            
        return seat_metrics_cons_df, seat_inv_final_df    

def seat_mgmt():
    seat_dataset1 = st.sidebar.file_uploader("Upload Bulk Upload File in XLSX format", type=["xlsx"], key="seat1")
    if seat_dataset1 is not None:

        #Open Seat Management File for Bulk Upload
        seat_df1 = file_excel_explore_data(seat_dataset1, key="seatsh1")
        
        #Replace Column Names
        seat_df1.columns = seat_df1.columns.str.replace(' ','_')
        # renaming the columns 
        seat_df1.rename(columns = {"Include_/_Exclude": "Include_Exclude"}, inplace = True) 
        seat_df1.rename(columns = {"Required_Cog_Laptop_(_YES/NO)": "Required_Cog_Laptop"}, inplace = True)
        seat_df1.rename(columns = {"Shared_Seat/Dedicated_Seat_Seat": "Shared_Dedicated_Seat"}, inplace = True)
        seat_df1['FTE'] = seat_df1['Percent_Allocation']/100.0
        seat_df1["Wing"].fillna("0", inplace = True)
        seat_df1['Associate_ID'] = pd.to_numeric(seat_df1['Associate_ID'], errors='coerce')
        seat_df1["Associate_ID"].fillna("0", inplace = True)
        
        seat_df1['Floor'] = pd.to_numeric(seat_df1['Floor'], errors='coerce')
        seat_df1["Floor"].fillna("0", inplace = True)
        seat_df1['Module'] = pd.to_numeric(seat_df1['Module'], errors='coerce')
        seat_df1["Module"].fillna("0", inplace = True)        

        seat_df1 = seat_df1.fillna(0).astype({"Floor":'int', "Module":'int', 'Associate_ID':'int'})
        #seat_df1 = seat_df1.fillna(0).astype({"Floor":'int', "Module":'int'})
        #seat_df1 = seat_df1.fillna(0, inplace=True)
        seat_df1['Floor_Wing_Module'] = seat_df1[['Floor','Wing', 'Module']].apply(lambda x : '{}Floor-{}Wing-{}ODC'.format(x[0],x[1],x[2]), axis=1)
        seat_df1['Seat_Type_Associate'] = seat_df1[['Associate_ID', 'Associate_Name', 'Shared_Dedicated_Seat',  \
                                                    'Cubicle_Type', 'Proposed_Seat_Details' \
                                                    ]].apply(lambda x : '{}-{}-{}-({})-{}'.format(x[0],x[1],x[2],x[3],x[4]), axis=1)
                
        #Map Designations   
        seat_df1 = seat_map_designations(seat_df1)
        
        #Default No Errors to start-with
        seat_df1['ErrorScenario'] = "NoError"
        
        #Count of Seats tagged
        seat_df1['Freq_Proposed_Seat_Details'] = seat_df1.groupby('Proposed_Seat_Details')['Proposed_Seat_Details'].transform('count')
        
        #Original DF
        #st.dataframe(seat_df1)
                
        col_names = ['LOB', 'Service_Grouping', 'Include_Exclude', 'Project_ID', 'Project_Description', 'Project_Manager_ID', 'Project_Manager_Name', \
                     'Account_ID', 'Account_Name', 'Associate_ID', 'Associate_Name', 'Designation', 'Grade', 'Department_Name', 'Location_ID', 'Country', \
                     'State', 'City', 'FTE', 'IMIS_Alloc', 'HCM_SetID', 'Seat_number', 'Assest_ID', 'Required_Cog_Laptop', \
                     'Base_Location', 'Revised_Location', \
                     'Floor_Wing_Module','Proposed_Seat_Details', 'Remarks', 'Shared_Dedicated_Seat', 'Cubicle_Type', 'Seat_Type_Associate', \
                     'Freq_Proposed_Seat_Details', 'ErrorScenario']   
        
        #Copy to revised DF 
        seat_df =  pd.DataFrame(seat_df1, columns=col_names)
                
        html_temp2 = """ <h4 style="color:{};text-align:left;">Seat View</h4> """
        st.markdown(html_temp2.format('royalblue','white'),unsafe_allow_html=True)
        
        #Display Revised DF
        if st.checkbox("Complete View of SEATs"):
            with st.beta_expander('Allocation with SEAT details..',expanded=False):
                st.dataframe(seat_df)
            
        #Check all Error Scenarios. Final result is in --> seat_err_df
        
        #Seat_df (original) whereas seat_filter_df is filtered DF 
        seat_filter_df = seat_df
        
        seat_err_df, seat_filter_df = seat_df_error_scenario(seat_df)

        #Write Error DataFrame
        if st.checkbox("Possible Error Scenarios"):
            st.dataframe(seat_err_df)     

            #enable download as hyperlink
            st.markdown(get_table_download_link(seat_err_df, seat_df, 'Error-Seat-Details', 'Total-Seats', 'Seat-Error-view'), unsafe_allow_html=True)         

        seat2_df = seat_df
        if st.checkbox("Want to see Summary View with Filter options?"): 
            seat_df, seat2_df = filter_seat_criteria(seat_df, seat2_df)

            #Display of various statistics
            dataframe_statistics(seat_df, seat2_df)

  
        #Build Seat Inventory details based on the allocation seat shared 
        if st.checkbox("Want to see Overall Utilization Metrics inclusive of Forecast/Digital Lock?"):        
            seat_metrics_cons_df, seat_inv_final_df = seat_utilization(seat_df, seat_filter_df)
        
            #enable download as hyperlink
            st.markdown(get_table_download_link_4df(seat_err_df, seat_metrics_cons_df, seat_inv_final_df, seat_df, \
                                                    'Error-Seat-Details', 'Seat_Metrics_View', 'Seat_ODC_Inventory', 'Total-Given-Seats', \
                                                    f'Overall-SeatMgmt'), unsafe_allow_html=True)
         

