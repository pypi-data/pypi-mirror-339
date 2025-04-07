#ifndef __DEXHAND_H__
#define __DEXHAND_H__

#include <iostream>
#include <memory>
#include "./hand/fhand.h"

using namespace hand_ws;
namespace FdHand
{
    enum class Ret
    {
        SUCCESS = 0,
        FAIL = -1,
        TIMEOUT = -2
    };
    class DexHand
    {
    private:
        void calibrationThread(std::string &ip);
        bool isValidIP(const std::string &ip);
        // public:
        Fhand *hand = new Fhand();

    public:
        DexHand();
        ~DexHand();

        Ret init(int flg = 0);

        std::vector<std::string> get_ip_list();
        std::string get_name(std::string ip);
        std::string get_type(std::string ip);
        std::string get_driver_ver(std::string ip);
        std::string get_hardware_ver(std::string ip);
        std::vector<long> get_errorcode(std::string ip);

        // opr
        Ret set_pos(std::string ip, std::vector<float> pos);
        std::vector<float> get_pos(std::string ip);
        Ret clear_errorcode(std::string ip);
        std::vector<std::vector<uint8_t>> get_ts_matrix(std::string ip);
        Ret fast_set_pos(std::string ip, std::vector<float> pos);

        Ret set_hand_config(std::string ip, std::string config);
        std::string get_hand_config(std::string ip);

        /**
         * @brief Get the position velocity current information
         * @param ip
         * @return std::vector<std::vector<float>>
         */
        std::vector<std::vector<float>> get_pvc(std::string ip);

#ifdef FDHX_TOOLS
        Ret set_pwm(std::string ip, std::vector<float> pwm);
#endif
        Ret reboot();
        Ret reboot(std::string ip);

        Ret enable();
        Ret enable(std::string ip);
        Ret disable();
        Ret disable(std::string ip);
        Ret calibration();
        Ret calibration(std::string ip);
    };
}
#endif
