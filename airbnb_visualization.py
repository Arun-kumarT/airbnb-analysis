import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from streamlit_folium import folium_static
# from pandas_profiling import ProfileReport
# from streamlit_pandas_profiling import st_profile_report

def dataframe():
    df= pd.read_csv("D:/projectyoutube/airbnb5.csv")
    df["latitude"]=df["latitude"].astype("float32")
    df["longitude"]=df["longitude"].astype("float32")
    return df

##sqlalchemy 
config = {'user':'root',    'host':'localhost','password':'1234', 'database':'airbnb'}
connection = mysql.connector.connect(**config)
cursor = connection.cursor()
engine = create_engine('mysql+mysqlconnector://root:1234@localhost/airbnb',echo=False)

with st.sidebar:
    select= option_menu("Main Menu", ["Home", "Booking","PRICE ANALYSIS","AVAILABILITY ANALYSIS","LOCATION BASED ANALYSIS", "EDA"])
df=dataframe()    
if select == "Home":
    
    st.title(":rainbow[Airbnb Analysis]")
        #import airbnb data
    
    st.dataframe(df)

elif select == "Booking":
    tab1,tab2,tab3=st.tabs(["Global listing of Hotels","Location","Hotel Insights"])
    with tab1:
        st.title("GEOSPATIAL VISUALIZATION")
        st.write("")


        fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', color='price', size='accomdates',
                        color_continuous_scale= "rainbow",hover_name='name',range_color=(0,49000), mapbox_style="carto-positron",
                        zoom=1)
        fig.update_layout(width=1150,height=800,title='Geospatial Distribution of Listings')
        st.plotly_chart(fig)
    with tab2:
        col1,col2 = st.columns(2)
        with col1:
            st.header(':red[🏨airbnb]')
            destination = st.selectbox('**Search destination**',('New York', 'Hawaii', 'Istanbul', 'Hong Kong', 'Sydney', 'Porto',
            'Rio De Janeiro', 'Montreal', 'Barcelona'),index=None,key='destination',placeholder='Select a destination')
            type = st.selectbox('**Select the property types**',['Apartment', 'Bed and breakfast', 'Guesthouse', 'Hostel',
            'Serviced apartment', 'Loft', 'House', 'Condominium', 'Treehouse',
            'Guest suite', 'Bungalow', 'Townhouse', 'Villa', 'Cabin', 'Other',
            'Farm stay', 'Chalet', 'Boutique hotel', 'Cottage', 'Boat',
            'Earth house', 'Aparthotel', 'Resort', 'Tiny house',
            'Nature lodge', 'Hotel', 'Camper/RV', 'Casa particular (Cuba)',
            'Barn', 'Hut', 'Heritage hotel (India)', 'Pension (South Korea)',
            'Campsite', 'Castle', 'Houseboat', 'Train'],index=None,key='type',placeholder='Select property type')
            
        with col2:
            st.header(":blue[Filter]")
            start, end = st.select_slider('**Select a price range in dollars**',
            options=['5', '50', '100', '200', '300', '500', '1000','2000', '5000', '10000', '20000', '50000'],
            value=('5', '200'))
            n_accommodates = st.slider('**Select number of people**', 1,16,step=1)
            n_bedrooms = int(st.select_slider('**Select number of bedrooms**', 
                options=['0','1','2','3','4','5','6','7','8','9','10','15','20']))
            rating = st.slider('**Select minimum rating**', 0,10,step=1)


        if destination is not None:

            #Selecting latitude and longitude for view state of map
            map_dict = {'New York': '-73.9652,40.7996', 'Hawaii': '-157.8208,21.2753', 'Istanbul': '28.9800,41.0062', 'Hong Kong': '114.1503,22.2816',
                'Sydney': '151.2155,-33.8803', 'Porto': '-8.6087,41.1543', 'Rio De Janeiro': '-43.1908,-22.9843', 'Montreal': '-73.5495,45.5455',
                'Barcelona': '2.1694,41.4008'}
            lon,lat = map(float,map_dict[destination].split(','))

            if type:
                condition = (df.city == destination) & (df.no_of_bedrooms == n_bedrooms) & (df.accomdates == n_accommodates) & (df.overall_review_score >= rating) & (df.price >= float(start)) & (df.price <= float(end)) & (df.property_type == type)
            else:
                condition = (df.city == destination) & (df.no_of_bedrooms == n_bedrooms) & (df.accomdates == n_accommodates) & (df.overall_review_score >= rating) & (df.price >= float(start)) & (df.price <= float(end))
            
            df_a = df[['name', 'address', 'property_type','host_name','accomdates','no_of_bedrooms','price','overall_review_score',"coordinates",'latitude', 'longitude']][condition].reset_index(drop=True)
            df_a.index += 1
            df_a = df_a.rename_axis('Index').reset_index()

            df_id = df[['id', 'name','price']][condition].reset_index(drop=True)
            df_id.index+=1

            st.write(":red[**Listings**]")
            st.dataframe(df_a,use_container_width=True,hide_index=True)

        if st.button("show location"):
                    m = folium.Map(location = [df_a['latitude'].mean(), 
                               df_a['longitude'].mean()], 
                    zoom_start=10)
                    # Create a MarkerCluster layer for better performance with many markers
                    marker_cluster = MarkerCluster().add_to(m)

    # Add markers for each Airbnb location
                    for index, row in df_a.iterrows():
                        popup_content = f"Name: {row['name']} \
                        <br>Price: ${row['price']} \
                        <br>Accommodates: {row['accomdates']}"
                        folium.Marker([row['latitude'], 
                        row['longitude']], 
                        popup=popup_content).add_to(marker_cluster)

                    try :
                        st.pydeck_chart(folium_static(m))
                    except Exception as e:
                         print('Error message' + str(e))

    with tab3:

            #Displaying property in detail
            number = st.text_input(label="**Enter the :red[Index] from the table to display the details of the property**",placeholder="example:1")
            button = st.button(label='Submit')
            if button:
                if number.isdigit():
                    index=int(number)
                    if index in df_id.index:
                        id = df_id.loc[index]['id']
                        df1 = df[df.id == id].reset_index(drop=True)
                        st.dataframe(df1)
                
                col1,col2 = st.columns(2)
                with col1:
                    st.write(":red[**Property Name**]")
                    st.write(df1.loc[0]['name'])
                    st.write(":red[**Address**]")
                    st.write(df1.loc[0]['address'])
                    st.write(":red[**Property Type**]")
                    st.write(df1.loc[0]['property_type'])
                    st.write(":red[**Description**]")
                    st.write(df1.loc[0]['amenities'])
                    st.write(":red[**Location Review**]")
                    st.write(df1.loc[0]['review_location'])
                    st.write(":red[**House rules**]")
                    st.write(df1.loc[0]['rules'])
                with col2:
                    page=df1.loc[0]['image']
                    st.page_link(page=page, label=":blue[**Picture**]")
                    st.write(":red[**Host Name**]")
                    col3,col4 = st.columns(2)
                with col3:
                    st.write(df1.loc[0]['host_name'])
                    
                    m = folium.Map(location = [df1['latitude'].mean(), 
                               df1['longitude'].mean()], 
                    zoom_start=10)
                    # Create a MarkerCluster layer for better performance with many markers
                    marker_cluster = MarkerCluster().add_to(m)

    # Add markers for each Airbnb location
                    for index, row in df1.iterrows():
                        popup_content = f"Name: {row['name']} \
                        <br>Price: ${row['price']} \
                        <br>Accommodates: {row['accomdates']}"
                        folium.Marker([row['latitude'], 
                        row['longitude']], 
                        popup=popup_content).add_to(marker_cluster)

                    try :
                        st.pydeck_chart(folium_static(m))
                    except Exception as e:
                         print('Error message' + str(e))

                


elif select == "PRICE ANALYSIS":
        
    st.title("**PRICE ANALYSIS**")
    tab1,tab2=st.tabs(["Analysis 1","Analysis2"])

    with tab1:
                
        country= st.selectbox("Select the Country",df["country"].unique())

        df1= df[df["country"] == country]
        df1.reset_index(drop= True, inplace= True)

        room_ty= st.selectbox("Select the Room Type",df1["room"].unique())
        
        df2= df1[df1["room"] == room_ty]
        df2.reset_index(drop= True, inplace= True)

        df_bar= pd.DataFrame(df2.groupby("property_type")[["price","overall_review_score","total_review"]].sum())
        df_bar.reset_index(inplace= True)

        fig_bar= px.bar(df_bar, x='property_type', y= "price", title= "PRICE FOR PROPERTY_TYPES",hover_data=["overall_review_score","total_review"],color_discrete_sequence=px.colors.sequential.Redor_r, width=600, height=500)
        st.plotly_chart(fig_bar)
    with tab2:
            
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        proper_ty= st.selectbox("Select the Property_type",df2["property_type"].unique())

        df4= df2[df2["property_type"] == proper_ty]
        df4.reset_index(drop= True, inplace= True)

        df_pie= pd.DataFrame(df4.groupby("cancel_policy")[["price","no_of_bedrooms"]].sum())
        df_pie.reset_index(inplace= True)

        fig_pi= px.pie(df_pie, values="price", names= "cancel_policy",
                        hover_data=["no_of_bedrooms"],
                        color_discrete_sequence=px.colors.sequential.BuPu_r,
                        title="PRICE DIFFERENCE BASED ON CANCALATION POLICY",
                        width= 600, height= 500)
        st.plotly_chart(fig_pi)

  
elif select=="AVAILABILITY ANALYSIS":
    
    country_a= st.selectbox("Select the Country",df["country"].unique())

    df1_a= df[df["country"] == country_a]
    df1_a.reset_index(drop= True, inplace= True)

    property_ty_a= st.selectbox("Select the Property Type",df1_a["property_type"].unique())
    
    df2_a= df1_a[df1_a["property_type"] == property_ty_a]
    df2_a.reset_index(drop= True, inplace= True)

    df_a_sunb1= px.sunburst(df2_a, path=["room","bed","address"], values="availability_365",width=600,height=500,title="Based on rooms,Type of bed,Location of property",color_discrete_sequence=px.colors.sequential.Peach_r)
    st.plotly_chart(df_a_sunb1)

elif select=="LOCATION BASED ANALYSIS":
    country_a= st.selectbox("Select the Country_a",df["country"].unique())

    df1_a= df[df["country"] == country_a]
    df1_a.reset_index(drop= True, inplace= True)

    property_ty_a= st.selectbox("Select the Property Type",df1_a["property_type"].unique())
    
    df2_a= df1_a[df1_a["property_type"] == property_ty_a]
    df2_a.reset_index(drop= True, inplace= True)
    df_a_sunb2= px.sunburst(df2_a, path=['availability_365','no_of_bedrooms','accomdates'],values='price',color='price',width=600,height=500,title="Based on availability,no of bedroom & no of people it can accommodates",color_discrete_sequence=px.colors.sequential.Peach_r)
    st.plotly_chart(df_a_sunb2)

elif select == "EDA":
        
        st.write("Exploratory data analysis")
        tab1,tab2=st.tabs(["Correlation","Variable distribution"])
        #EDA using pandas-profiling
        # profile = ProfileReport(pd.read_csv('airbnb.csv'), explorative=True)

        # #Saving results to a HTML file
        # # pr=profile.to_file("output.html")
        # st_profile_report(profile)
        with tab1:
            st.header(":red[Correlation using Heatmap]")
            dff = df[["price","accomdates","overall_review_score","review_val","guest","min_night","max_night","no_of_bathroom","no_of_bedrooms"]]

            correlation_matrix = dff.corr()

            fig = px.imshow(correlation_matrix, text_auto=True, aspect="auto",color_continuous_scale="reds")

            fig.update_layout(coloraxis_colorbar=dict(title="Correlation"))

            st.plotly_chart(fig, use_container_width=True)

            d = {"Category":[],"Min":[],"Max":[],"Mean":[],"Median":[],"Mode":[],"Standard Deviation":[]}

            for i in ["price","accomdates","overall_review_score","review_val","guest","min_night","max_night","no_of_bathroom","no_of_bedrooms"]:
                d["Category"].append(i)
                d["Min"].append(min(df[i]))
                d["Max"].append(max(df[i]))
                d["Mean"].append(int(df[i].mean()))
                d["Median"].append(df[i].median())
                d["Mode"].append(df[i].mode()[0])
                d["Standard Deviation"].append(df[i].std())

            df = pd.DataFrame(d)
            with st.expander("Do you like to see statistical data"):
                st.dataframe(df)
        with tab2:
            # fig=dabl.plot(df,target_col="price")
            # st.pyplot(fig)
            # image=st.image("D:\projectyoutube\analysis.png")
            st.image('analysis.png')

            
    

       
 