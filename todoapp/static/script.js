const deadlinesElements = document.querySelectorAll('.deadline');

//  checking if any of deadlines has value expired if
//  so change color to red
deadlinesElements.forEach(function(deadline){
    if(deadline.textContent === 'Failed'){
        deadline.classList.add('expired');
    }
})