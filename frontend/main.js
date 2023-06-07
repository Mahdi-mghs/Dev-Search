
let projectURL = 'http://127.0.0.1:8000/api/projectsapi/'

let token = localStorage.getItem('token')
let loginBtn = document.getElementById('login-btn')
let logoutBtn = document.getElementById('logout-btn')

if (token) {
    loginBtn.remove()
}else{
    logoutBtn.remove()
}

logoutBtn.addEventListener('click', (e) => {
    e.preventDefault()
    localStorage.removeItem('token')
    window.location = 'file:///home/kali/Public/frontend/login.html'
})

let getProjects = () => {

    fetch(projectURL)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        buildProject(data)
    })

}

let buildProject = (projects) => {
    let projectWrapper = document.getElementById("project-wrapper")
    projectWrapper.innerHTML = ''
    for (let i = 0; i < projects.length; i++) {
        let project = projects[i];
        
        let projectCard = `
        <div class="project--card">
            <img src="http://127.0.0.1:8000${project.img_file}" />
        
            <div>
                <div class="card--header">
                    <h3>${project.title}</h3>
                    <strong class="vote--option" data-vote="up" data-project="${project.id}" >&#43;</strong>
                    <strong class="vote--option" data-vote="down" data-project="${project.id}"  >&#8722;</strong>
                </div>
                <i>${project.vote_ratio}% Positive feedback </i>
                <p>${project.description.substring(0, 150)}</p>
            </div>
    
        </div>
        `
        projectWrapper.innerHTML += projectCard
    }
    addVoteEvent()
}

let addVoteEvent = () => {
    let cVote = document.getElementsByClassName('vote--option')
    let token = localStorage.getItem('token')
    for (let i = 0; i < cVote.length; i++) {
        cVote[i].addEventListener('click', (e) => {
            let vote = e.target.dataset.vote
            let project = e.target.dataset.project
            console.log('VOTE:', vote, 'ID:', project)

            fetch(`http://127.0.0.1:8000/api/projectapi/${project}/vote/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({ 'value': vote })
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data)
                    getProjects()
                })
        });
        
    }
}

getProjects()