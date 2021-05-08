#include<iostream>
#include<string>
using namespace std;
int main()
{  

    string ip,op1,op2,temp;
    int sizes[10] = {};
    char c;
    int n,j,l;
    cout<<"Enter The Parent Variable (Non-Terminal) : \n";
    cin>>c;
    ip.push_back(c);
    op1 += ip + "\'->";
    ip += "->";
    op2+=ip;
    cout<<"Enter The No. Of Productions : \n";
    cin>>n;
    for(int i=0;i<n;i++)
    {   cout<<"Enter Production "<<i+1<<": \n";
        cin>>temp;
        sizes[i] = temp.size();
        ip+=temp;
        if(i!=n-1)
            ip += "|";
    }
    cout<<"\nGiven Grammar : \n"<<ip<<endl;
    cout<<"\nLeft Recurssion : \n";
    for(int i=0,k=3;i<n;i++)
    {
        if(ip[0] == ip[k])
        {
            
            if(ip[k] != '#')
            {
                for(l=k+1;l<k+sizes[i];l++)
                    op1.push_back(ip[l]);
                k=l+1;
                op1.push_back(ip[0]);
                op1 += "\'|";
            }
        }
        else
        {
            
            if(ip[k] != '#')
            {
                for(j=k;j<k+sizes[i];j++)
                    op2.push_back(ip[j]);
                k=j+1;
                op2.push_back(ip[0]);
                op2 += "\'";
            }
            else
            {
                op2.push_back(ip[0]);
                op2 += "\'";
            }}}
    op1 += "ϵ";
    cout<<op2<<endl;
    cout<<op1<<endl;
    return 0;
}