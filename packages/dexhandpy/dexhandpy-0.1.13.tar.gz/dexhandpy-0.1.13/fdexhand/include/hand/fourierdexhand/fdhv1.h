#ifndef __FDHV1_H__
#define __FDHV1_H__

#include "basehand.h"

namespace BaseHandProtocol
{
    class Fdhv1 : public BaseHand
    {
    private:
        std::string ip_;
        uint32_t wait_replt_counts_max = 100000;
        std::vector<float> max_limited;

    public:
        Fdhv1(std::string ip);
        ~Fdhv1();

        FdhReturnCode calibration() override;
        FdhReturnCode enable() override;
        FdhReturnCode disable() override;
        FdhReturnCode reboot() override;

        FdhReturnCode get_cnt(std::vector<long> &fdb) override;
        FdhReturnCode get_pos(std::vector<float> &fdb) override;
        FdhReturnCode get_current(std::vector<float> &fdb) override;
        FdhReturnCode get_velocity(std::vector<float> &fdb) override;

        FdhReturnCode get_errorcode(std::vector<long> &fdb) override;
        FdhReturnCode get_status(std::vector<uint8_t> &fdb) override;
        FdhReturnCode clear_errorcode() override;

        FdhReturnCode get_comm_config(std::string &cfg) override;
        FdhReturnCode set_comm_config(std::string cfg) override;

        FdhReturnCode get_pos_limited(std::vector<float> &fdb) override;
        FdhReturnCode get_velocity_limited(std::vector<float> &fdb) override;
        FdhReturnCode get_current_limited(std::vector<float> &fdb) override;

        FdhReturnCode set_velocity_limited(uint8_t id, float max_speed) override;
        FdhReturnCode set_pos_limited(uint8_t id, float start_angel, float end_angle) override;
        FdhReturnCode set_current_limited(uint8_t id, float max_current) override;

        FdhReturnCode set_pos(std::vector<float> _cmd) override;
        FdhReturnCode set_velocity(std::vector<float> _cmd) override;
        FdhReturnCode set_current(std::vector<float> _cmd) override;

        FdhReturnCode fast_set_positions(std::vector<float> pos) override;
#ifdef FDHX_TOOLS
        FdhReturnCode set_pwm(std::vector<float> _cmd) override;
        FdhReturnCode fast_set_pwm(std::vector<float> pwm);
#endif

        FdhReturnCode get_ts_matrix(std::vector<std::vector<uint8_t>> &matrix) override;
        FdhReturnCode get_ts_tashan(std::vector<std::vector<float>> &tashan) override;
        FdhReturnCode get_ntc(int &temp) override;


        FdhReturnCode set_sn(std::string sn);
        FdhReturnCode set_mac(std::vector<int> mac);
        FdhReturnCode set_ip(std::vector<int> ip);

        FdhReturnCode reset_pid();

        FdhReturnCode set_pos_pid(uint8_t id, std::vector<float> _pid);
        FdhReturnCode set_velocity_pid(uint8_t id, std::vector<float> _pid);
        FdhReturnCode set_current_pid(uint8_t id, std::vector<float> _pid);

        FdhReturnCode get_pvc(std::vector<std::vector<float>> &fdb);
    };
}
#endif
