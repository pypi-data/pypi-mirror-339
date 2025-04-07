#ifndef __FHAND_H__
#define __FHAND_H__

#include "./fourierdexhand/basehand.h"
#include "./fourierdexhand/inspire.h"
#include "./fourierdexhand/fdhv1.h"
#include "./fourierdexhand/fdhv2.h"

using namespace BaseHandProtocol;

namespace hand_ws
{
    typedef enum
    {
        NONE,
        FDHV1_LEFT,
        FDHV1_RIGHT,
        FDHV2_LEFT,
        FDHV2_RIGHT,
        INSPIRE_LEFT,
        INSPIRE_RIGHT,
    } OperatePtrType;
    class Fhand
    {
    public:
        std::vector<std::unique_ptr<BaseHand>> hand_ptr;
        std::vector<std::string> ip_unique, type, name, driver_ver, hardware_ver, sn;
        std::vector<std::vector<unsigned int>> mac;

    private:
        std::vector<std::string> ip;
#ifndef FDHX_TOOLS
        socklen_t sockaddr_len = sizeof(struct sockaddr_in);
#endif
        enum class HandType
        {
            FDHV1 = 1,
            FDHV2,
            INSPIRE
        };

    private:
        FdhReturnCode is_duplicate_types();
        FdhReturnCode remove_repeated_types();

        FdhReturnCode broadcast();
        FdhReturnCode find_hand();

    public:
        Fhand(/* args */);
        ~Fhand();

        FdhReturnCode init();
        FdhReturnCode get_operate_pointer(std::vector<void *> &ptr_list, std::vector<OperatePtrType> &type);

        FdhReturnCode get_status(std::string _ip, std::vector<uint8_t> &status);
        FdhReturnCode get_errorcode(std::string _ip, std::vector<long> &errorcode);
        FdhReturnCode clear_errorcode(std::string _ip);

        FdhReturnCode calibration(std::string _ip);
        FdhReturnCode enable(std::string _ip);
        FdhReturnCode disable(std::string _ip);
        FdhReturnCode reboot(std::string _ip);

        FdhReturnCode set_position(std::string _ip, std::vector<float> position);
        FdhReturnCode get_position(std::string _ip, std::vector<float> &position);
        FdhReturnCode fast_set_positon(std::string _ip, std::vector<float> position);

        /**
         * @brief get the pvc (position, velocity, current)
         * @param _ip
         * @param pvc position, velocity, current
         * @return FdhReturnCode
         */
        FdhReturnCode get_pvc(std::string _ip, std::vector<std::vector<float>> &pvc);

#ifdef FDHX_TOOLS
        FdhReturnCode set_pwm(std::string _ip, std::vector<float> pwm);
#endif

        FdhReturnCode get_ts_matrix(std::string _ip, std::vector<std::vector<uint8_t>> &ts_matrix);

        FdhReturnCode get_comm_config(std::string _ip, std::string &config);
        FdhReturnCode set_comm_config(std::string _ip, std::string config);
    };

}
#endif
