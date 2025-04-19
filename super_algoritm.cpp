#include <iostream>
#include <fstream>
#include <map>
#include <vector>
#include <algorithm>

using namespace std;

unsigned short int kol_Kont, kol_Poezdov, b;
float cof;

map<int, string> id_name_Poezdov;                   // id поезда -> name поезда                     +
map<int, string> id_name_Kont;                      // id контейнера -> name контейнера             +

map<int, vector<int>> kon_poezda;                   // id Kont -> vector <poezd>                    +
map<int, int> kon_poezda_weight;                    // id Kont -> вес контейнера                    +

map<int, vector<int>> Kont_Poezd_answer;            // id поезда -> id контейнеров                  -
unsigned int answer_int = 1e18;                     // оценка случая ответ                          const

map<int, vector<int>> Poezd_Kont_prom;              // id поезда -> id контейнеров                  -
vector<bool> Kont_prom_flag;                        // флаги контейнеров                            +

unsigned int delta(){
    unsigned int mn = 1e18, mx = 0;

    for (int i=0; i<kol_Poezdov;i++){
        int sum_q = 0;
        for (int j=0; j<Poezd_Kont_prom[i].size();j++){
            sum_q += kon_poezda_weight[Poezd_Kont_prom[i][j]];
        }

        if (mx <= sum_q){
            mx = sum_q;
        }

        if (mn >= sum_q){
            mn = sum_q;
        }
    }

    return mx / (mx - mn);
}

unsigned int raz(){
    vector<string> v{};
    unsigned int k = 0;
    for (int i=0; i<kol_Kont; i++){
        string f = "  ";
        f[0]=id_name_Kont[i][4];
        f[1]=id_name_Kont[i][5];
        v.push_back(f);
    }

    sort(v.begin(), v.end());
    for (int i=0; i<kol_Poezdov-1; i++){
        if (v[i]!=v[i+1]){
            k++;
        }
    }
    return k + 1;
}

bool fin(){
    for (int i=0; i<kol_Kont; i++){
        if (Kont_prom_flag[i]){
            return false;
        }
    }

    return true;
}

void rec(int x){
    if (x == kol_Kont && fin()){
        for (int l=0; l<kol_Poezdov-1; l++){
            if (Kont_Poezd_answer[l]!=Kont_Poezd_answer[l+1]){
                return;
            }
        }
        if (delta() * cof + raz() <= answer_int){
            Kont_Poezd_answer = Poezd_Kont_prom;
            answer_int = delta() * cof + raz();
        }
    }

    Kont_prom_flag[x] = false;

    for (int i=0; i<kon_poezda[x].size();i++){
        Poezd_Kont_prom[kon_poezda[x][i]].push_back(x);
        rec(x+1);
        Poezd_Kont_prom[kon_poezda[x][i]].pop_back();
    }

    return;
}

int weight_zxc(int i){
    return (id_name_Kont[i][6]-'0')*10000 + (id_name_Kont[i][7]-'0')*1000 + (id_name_Kont[i][8]-'0')*100 + (id_name_Kont[i][9]-'0')*10 + (id_name_Kont[i][10]-'0');
}

int main(){
    ifstream inp("input1.txt");
    inp >> kol_Kont >> b >> cof;
    inp.close();

    ifstream pqla("input2.txt");
    string s;


    int p;
    Kont_prom_flag.resize(kol_Kont, true);

    for (int i=0; i<kol_Kont; i++){
        pqla >>s;
        pqla >>s;
        pqla >>s;
        id_name_Kont[i] = s;

        pqla >>s;pqla >>s;pqla >>s;

        int k=0;

        while (pqla>>s>>p){
            if (p<b){
                kon_poezda[i].push_back(k);
            }
            id_name_Poezdov[i] = s;
            k++;
        }

        kol_Poezdov = k;
    }

    for (int i=0;i<kol_Kont;i++){
        kon_poezda_weight[i] = weight_zxc(i);
    }

    pqla.close();

//_____________________________________________________________________________________________________________________________
    rec(0);
//_____________________________________________________________________________________________________________________________

    ofstream ou("output.csv");
    b=0;

    
    for (int i=0; i<kol_Kont; i++){
        for (int j=0; j<kol_Poezdov; j++){
            if (find(Kont_Poezd_answer[j].begin(), Kont_Poezd_answer[j].end(), i) != Kont_Poezd_answer[j].end()){
                b=j;
            }
        }

        ou << id_name_Kont[i] << "                      "<< id_name_Poezdov[b]<<'\n';
    }

    ou.close();
}
