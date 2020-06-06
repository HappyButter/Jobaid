const filterOffersBtn = document.querySelector('.form__submit');
const technologiesInput = document.querySelector('.technologies__input');
const experienceSelect = document.querySelector('.experience__select');
const locationInput = document.querySelector('.location__input');
const b2bCheckbox = document.querySelector('.contracts__container input[name="b2b"]');
const uopCheckbox = document.querySelector('.contracts__container input[name="uop"]');
const salaryMinInput = document.querySelector('.salary__container input[name="fork_min"]');
const salaryMaxInput = document.querySelector('.salary__container input[name="fork_max"]');

const gatherUserInput = () => {
    return {
        technologies: technologiesInput.value ? technologiesInput.value.split(",").map(item => item.trim()) : [],
        experience: experienceSelect.value,
        location: locationInput.value,
        b2b: b2bCheckbox.checked,
        uop: uopCheckbox.checked,
        salaryMin: salaryMinInput.value,
        salaryMax: salaryMaxInput.value,
    }
}

const createFilterUrl = filters => {
    let url = window.location.href;
    console.log(url);
    url += url.indexOf('?') === -1 ? '?' : '';
    const page_index = url.indexOf('page');
    const filters_index = url.indexOf('&');
    if (page_index !== -1 && filters_index !== -1)
        url = url.substr(0, (page_index > filters_index ? filters_index : page_index));

    console.log(url); 
    console.log(filters.technologies); 
    filters.technologies.length ? url += `&technologies=${filters.technologies.join(',')}` : null;
    console.log(url);
    filters.experience ? url += `&experience=${filters.experience}` : null;
    filters.location ? url += `&location=${filters.location}` : null;
    filters.uop ? url += `&uop=true` : null;
    filters.b2b ? url += `&b2b=true` : null;
    filters.salaryMin ? url += `&fork_min=${filters.salaryMin}` : null;
    filters.salaryMax ? url +=`&fork_max=${filters.salaryMax}` : null;
    console.log(url)
    url = url.replace('#', 'sharp');

    return url;
}

filterOffersBtn.addEventListener('click', e => {
    e.preventDefault();

    const filters = gatherUserInput();
    const url = createFilterUrl(filters);

    window.location.assign(url);
});
