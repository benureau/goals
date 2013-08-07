#ifndef _CDATASET_H_
#define _CDATASET_H_

#include <vector>
#include <queue>

class _cSeigel {
    public:
        _cSeigel(int span);

        void add(double v);
        double beta();

        int size();
        void reset();

    private:
        double _beta;
        int _span;
        int _last_compute;

        std::vector<double> _data;
        std::vector<std::vector<double> > _slopes;

        void _recompute();
};

#endif // _CDATASET_H_
