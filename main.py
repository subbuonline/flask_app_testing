from flask import Flask, request, jsonify,send_file
from io import BytesIO
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
app = Flask(__name__)




def dhelli_court1(from_date,to_date):
    # from_date='01/01/1953'
    # to_date='17/05/2023'
    baseurl='http://164.100.69.66/jsearch/'
    
    # getting the number of total records available
    
    get_total_records='http://164.100.69.66/jsearch/title1.php?page={}&scode=31&fflag=1&titlesel=O&p_name=&frdate={}&todate={}'.format(1,from_date,to_date)
    output_data=requests.get(get_total_records)
    soup1 = BeautifulSoup(output_data.text, 'html.parser')
    total_records=soup1.find('td', attrs={'align': 'left','colspan':'1'}).b
    digit = re.findall(r'\d', total_records.text)
    total=''.join(digit)
    iterations=int(total)//28+1
   
   
    data_collection=[]
   
    for page in range(1,iterations):
        
        data_link='http://164.100.69.66/jsearch/title1.php?page={}&scode=31&fflag=1&titlesel=O&p_name=&frdate={}&todate={}'.format(page,from_date,to_date)
        response=requests.get(data_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        data=soup.find('table', attrs={'width': '100%','border':'1','bgcolor':'#FFFFFF'})
       
        rows = data.find_all('tr')
        print(page)
        for row in rows:
          
           data_dict={}
           
           data_dict['Page Number']=page
           data_dict['URL']=data_link
           cells=row.find_all('td')
           if(len(cells)==6):
                
                links = cells[2].find_all('a')
                try: data_dict['slno']=cells[0].text
                except: data_dict['slno']=''
               
                try:data_dict['Case No']=cells[1].text
                except:data_dict['Case No']=''
                
                try:data_dict['Judgement Date']=cells[2].text.split('(')[0]
                except:data_dict['Judgement Date']=''
                
                try: data_dict['Party']=cells[3].text
                except:data_dict['Party']=''
                
                try:data_dict['Corrigendum']=cells[4].text.strip()
                except:data_dict['Corrigendum']=''
                
            
               
                
                
                data_dict['Query From']=from_date
                data_dict['Query To']=to_date
               
                try:
                    data_dict['PDF']=links[0]['href']
                except:
                    data_dict['PDF']=''
                try:
                    
                    data_dict['Text File']=links[1]['href']
                except:
                    data_dict['Text File']=''
            
                    
              
                data_collection.append(data_dict)
         
            
    df=pd.DataFrame(data_collection)
    output = BytesIO()
    df.to_excel(output, index=False, encoding='utf-8')
    output.seek(0)
    
    return output
    


@app.route('/dhelli_court1', methods=['GET'])
def dhelli_court2():
    from_date = request.args.get('fromDate')
    to_date = request.args.get('toDate')
    output=dhelli_court1(from_date,to_date)
    
    return send_file(output, mimetype='text/xlsx', as_attachment=True, download_name='data.csv')


if __name__ == '__main__':
    app.run()
