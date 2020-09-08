

var app = new Vue({
    delimiters: ['{!', '}}'],
    el: '#app',
    data: {
        check_ins: '',
        loading: true,
        messages: []
    },

    methods: {
        sendReadyNotifcation: function (i, index) {
            axios({
                method: 'get',
                url: '/send_ready_notification',
                params: {
                    pk: i.pk
                }
            })
                .then(response => {
                    console.log(response['data']);
                    this.check_ins = response['data']['check_ins'];
                    this.messages = this.messages.concat(response['data']['message'])
                })
                .catch(error => {
                    alert('Random Error has occurred. Refresh Page!')
                    console.log(error);
                    this.errored = true
                })
                .finally(() => {
                        $(document).ready(function(){
                            $('.toast').toast('show');
                        });
                })
        },

        cancelCheckin: function (i) {
            axios({
                method: 'get',
                url: '/cancel_checkin',
                params: {
                    pk: i.pk
                }
            })

                .then(response => {
                    console.log(response['data']['message'])
                    this.check_ins = response['data']['check_ins'];
                    this.messages = this.messages.concat(response['data']['message'])
                })
                .catch(error => {
                    alert('Random Error has occurred. Refresh Page!')
                    console.log(error);
                    this.errored = true
                })
                .finally(() => {
                    $(document).ready(function(){
                        $('.toast').toast('show');
                    });
                })

        }
    },

    mounted() {
        let x = window.location.pathname;
        let url = '/get_check_ins';

        // Send a POST request
        axios({
            method: 'post',
            url: url,
            data: {
            }
        })

        .then(response => {
            this.check_ins = response['data'];
        })
        .catch(error =>{
            console.log(error);
            this.errored = true
        })
        .finally(() => this.loading = false)

    }
});



