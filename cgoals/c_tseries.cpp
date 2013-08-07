#include <algorithm>
#include <cmath>
#include "c_tseries.h"

using namespace std;

_cSeigel::_cSeigel(int span) {
    _span = span;
    _last_compute = 0;
}

void _cSeigel::add(double value) {
    _data.push_back(value);
    _last_compute = max(_last_compute, int(_data.size()) - _span);
}

int _cSeigel::size() {
    return _data.size();
}

void _cSeigel::reset() {
}

double median(vector<double> data, int span) {
    // printf("data      ");
    // for (int i = 0; i< data.size(); i++) {
    //     printf("%+.2f, ", data[i]);
    // }
    // puts("");
    vector<double> data_copy(span);
    for (int i = 1; i <= span; i++){
        data_copy[i-1] = data[data.size()-i];
    }
    sort(data_copy.begin(), data_copy.end());
    // printf("data_copy ");
    // for (int i = 0; i< data_copy.size(); i++) {
    //     printf("%+.2f, ", data_copy[i]);
    // }
    // puts("");

    if (span % 2 == 0)
        return (data_copy[int(span/2-1)] + data_copy[int(span/2)])/2;
    else
        return data_copy[int((span-1)/2)];
}

void _cSeigel::_recompute() {

    for(int n = _last_compute; n < _data.size(); n++) {
        double v = _data[n];
        vector<double> new_slopes = vector<double>();
        _slopes.push_back(new_slopes);

        for (int i = max(0, int(_data.size())-_span); i < n; i++) {
            double slope_ni = (v - _data[i])/(n-i);
            _slopes[i].push_back(slope_ni);
            _slopes[n].push_back(slope_ni);
        }
    }

    // for(int k = 0; k < _slopes.size(); k++) {
    //     printf("slope %d ", k);
    //     for (int i = 0; i < _slopes[k].size(); i++) {
    //         printf("%+.2f, ", _slopes[k][i]);
    //     }
    // puts("");
    // }

    int span = min(int(_data.size()), _span);
    vector<double> medians = vector<double>(span);
    for (int j = 1; j <= span; j++) {
        medians[j-1] = median(_slopes[_slopes.size()-j], span-1);
    }

    _beta = median(medians, span);
    _last_compute = _data.size();

}

double _cSeigel::beta(){
    if (_data.size() < 2) {
        return 0.0;
    }
    if (_last_compute < int(_data.size())) {
        this->_recompute();
    }
    return _beta;
}
