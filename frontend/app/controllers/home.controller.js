export default function HomeController($scope, AnswerService) {

    this.question = "";
    this.answers = [""];

    this.ask = function () {
        AnswerService.ask(this.question).then(response => {
            for (let arr of response) {
                for (let elem of arr) {
                    this.answers.push(elem);
                }
            }
            $scope.$apply()
        })
    }
}
