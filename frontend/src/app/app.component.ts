import { Component, OnChanges, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import {FormArray, FormBuilder, FormGroup, Validators} from '@angular/forms';
import { QuestionService } from 'src/app/services/question.service';
import { constants } from 'src/config';
import { CandidateService } from 'src/app/services/candidate.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { catchError, of } from 'rxjs';
import { MatStepper } from '@angular/material/stepper';
import { CandidateInterface } from './interfaces/candidate.interface';
import { ApplicationService } from './services/application.service';
import { ApplicationInterface } from './interfaces/application.interface';
import { AnswerInterface } from './interfaces/answer.interface';
import { QuestionInterface } from './interfaces/question.interface';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
    @ViewChild('stepper') stepper!: MatStepper;
    isLinear = true;

    loginFormGroup = this._formBuilder.group({
        cpf: ['', [Validators.required, Validators.minLength(11), Validators.maxLength(11)]],
        password: ['', Validators.required],
    });

    infoFormGroup = this._formBuilder.group({
        email: ['', [Validators.required, Validators.email]],
        full_name: ['', Validators.required],
        age: ['', Validators.required],
        father_name: [''],
        mother_name: [''],
        gender: ['', Validators.required],
        phone: ['', Validators.required],
        religion: [''],
    });

    regionFormGroup = this._formBuilder.group({
        country_region: ['', Validators.required],
    });

    midiaFormGroup = this._formBuilder.group({
        video_url: [''],
        photo1_url: [''],
        photo2_url: [''],
        photo3_url: [''],
    });

    sectionsFormGroup = this._formBuilder.group({});

    groupedQuestions: any = [];

    candidate?: CandidateInterface;
    application?: ApplicationInterface;

    constructor(
        private _formBuilder: FormBuilder,
        private _questionService: QuestionService,
        private _candidateService: CandidateService,
        private _applicationService: ApplicationService,
        private _snackBar: MatSnackBar
    ) { }

    ngOnInit() {

        this._questionService.getQuestions(constants.SEASON).subscribe((data: any) => {

            const groupedQuestions = data.reduce((acc: any, question: any) => {
                const section = question.form_section;
                if (!acc[section]) {
                    acc[section] = [];
                }
                acc[section].push(question);
                return acc;
            }, {});

            this.groupedQuestions = Object.keys(groupedQuestions)
                .map(section => ({

                    section: section,
                    title: section,
                    questions: groupedQuestions[section]

                }));

            this.groupedQuestions.forEach((group: any) => {

                const groupForm: FormGroup = this._formBuilder.group({});

                group.questions.forEach((question: any) => {
                    groupForm.addControl(
                        `${question.id}`,
                        this._formBuilder.control('')
                    );
                });

                this.sectionsFormGroup.addControl(group.section, groupForm);
            });

        });

    }

    nextStep() {
        const nextStep = this.stepper.selectedIndex + 1;
        if (nextStep < this.stepper.steps.length) {
            //this.stepper.selected.completed = true;
            this.stepper.selectedIndex = nextStep;
        }
    }

    login(){
        this._candidateService.login(
            this.loginFormGroup.get('cpf')?.value!,
            this.loginFormGroup.get('password')?.value!)
                .pipe(catchError((err: any) => {
                    if(err.status === 404){
                        return of(null);
                    } else {
                        this._snackBar.open(err.error.detail ?? 'Não autorizado', 'OK');
                        throw err;
                    }
                }))
                .subscribe((data: any) => {
                    if(data){
                        this.candidate = data;
                        this.infoFormGroup.patchValue(data);
                        this.getApplication();
                        this.isLinear = false;
                        this.loginFormGroup.disable();
                    } else
                        this._snackBar.open('Preencha a próxima etapa para salvar seu cadastro', 'OK');

                    this.nextStep();
                }
        );
    }

    logout(){
        this.stepper.reset();
        this.isLinear = true;
        this.candidate = undefined;
        this.application = undefined;
        this.loginFormGroup.reset();
        this.infoFormGroup.reset();
        this.regionFormGroup.reset();
        this.midiaFormGroup.reset();
        this.sectionsFormGroup.reset();
        this.loginFormGroup.enable();
        this.loginFormGroup.enable();
        this.infoFormGroup.enable();
        this.regionFormGroup.enable();
        this.midiaFormGroup.enable();
        this.sectionsFormGroup.enable();
    }

    createOrUpdateCandidate(){
        if(!this.isEntregue()){
            const data = {...this.loginFormGroup.value, ...this.infoFormGroup.value};
            if(this.candidate?.id){
                this._candidateService.update(this.candidate?.id, data)
                    .pipe(catchError((err: any) => {
                        this._snackBar.open(err.error.detail ?? 'Erro ao atualizar cadastro', 'OK');
                        throw err;
                    }))
                    .subscribe((data: any) => {
                        this._snackBar.open('Cadastro atualizado com sucesso', 'OK');
                        this.nextStep();
                    });
            } else {
                this._candidateService.create(data)
                    .pipe(catchError((err: any) => {
                        this._snackBar.open(err.error.detail ?? 'Erro ao criar cadastro', 'OK');
                        throw err;
                    }))
                    .subscribe((data: any) => {
                        this.candidate = data;
                        this._snackBar.open('Cadastro criado com sucesso', 'OK');
                        this.nextStep();
                    });
            }
        } else
            this.nextStep();
    }

    getApplication(){
        this._candidateService.getApplication(this.candidate?.id!, constants.SEASON)
            .pipe(catchError((err: any) => {
                if(err.status === 404){
                    return of(null);
                } else {
                    this._snackBar.open(err.error.detail ?? 'Erro ao buscar inscrição', 'OK');
                    throw err;
                }
            }))
            .subscribe((data: any) => {
                if(data){
                    this.application = data;
                    this.regionFormGroup.patchValue(data);
                    this.midiaFormGroup.patchValue(data);
                    this.getAnswers();
                    this.disableForms();
                }
            });
    }

    createOrUpdateApplication(){
        if(!this.isEntregue()){
            const data = {
                program_season: constants.SEASON,
                status: this.application?.status ?? constants.APPLICATION_STATUS.PENDENTE,
                ...this.regionFormGroup.value,
                ...this.midiaFormGroup.value
            };
            if(this.application?.id){
                this._applicationService.update(this.application?.id, data)
                    .pipe(catchError((err: any) => {
                        this._snackBar.open(err.error.detail ?? 'Erro ao atualizar inscrição', 'OK');
                        throw err;
                    }))
                    .subscribe((data: any) => {
                        this.nextStep();
                    });
            } else {
                this._applicationService.create(this.candidate?.id!, data)
                    .pipe(catchError((err: any) => {
                        this._snackBar.open(err.error.detail ?? 'Erro ao criar inscrição', 'OK');
                        throw err;
                    }))
                    .subscribe((data: any) => {
                        this.application = data;
                        this._snackBar.open('Inscrição iniciada, responda as perguntas', 'OK');
                        this.nextStep();
                    });
            }
        } else
            this.nextStep();
    }

    getAnswers(){
        this._applicationService.getAnswers(this.application?.id!)
            .pipe(catchError((err: any) => {
                if(err.status === 404){
                    return of(null);
                } else {
                    this._snackBar.open(err.error.detail ?? 'Erro ao buscar respostas', 'OK');
                    throw err;
                }
            }))
            .subscribe((data: any) => {
                if(data){
                    const resultObj: any = {};
                    for (const item of data) {
                        resultObj[item.question_id] = item.answer_text;
                    }
                    Object.keys(this.sectionsFormGroup.value).forEach((key) => {
                        this.sectionsFormGroup.get(key)?.patchValue(resultObj);
                    });
                }
            });
    }

    createOrUpdateAnswers(){

        if(!this.isEntregue()){

            const answers = [];
            const formSectionsValues: any = this.sectionsFormGroup.value;

            for (const section in formSectionsValues) {
                if (Object.prototype.hasOwnProperty.call(formSectionsValues, section)) {
                    const formSectionValue = formSectionsValues[section];
                    for (const question_id in formSectionValue) {
                        if (
                            Object.prototype.hasOwnProperty.call(
                                formSectionValue,
                                question_id
                            )
                        ) {
                            const answer_text = formSectionValue[question_id];
                            if(answer_text)
                                answers.push({
                                    question_id: question_id,
                                    answer_text: answer_text,
                                });
                        }
                    }
                }
            }

            if(this.application?.id){
                this._applicationService.postAnswers(this.application?.id, answers)
                    .pipe(catchError((err: any) => {
                        this._snackBar.open(err.error.detail ?? 'Erro ao salvar respostas', 'OK');
                        throw err;
                    }))
                    .subscribe((data: any) => {
                        this.nextStep();
                    });
            }

        } else
            this.nextStep();
    }

    finalizeApplication(){
        if(this.midiaFormGroup.get('video_url')?.value && this.midiaFormGroup.get('photo1_url')?.value){
            this._snackBar.open('Tem certeza que deseja finalizar a inscrição?', 'Sim', {
                duration: 10000,
            }).onAction().subscribe(() => {
                const data = {
                    status: constants.APPLICATION_STATUS.ENTREGUE,
                };
                if(this.application?.id){
                    this._applicationService.update(this.application?.id, data)
                        .pipe(catchError((err: any) => {
                            this._snackBar.open(err.error.detail ?? 'Erro ao finalizar inscrição', 'OK');
                            throw err;
                        }))
                        .subscribe((data: any) => {
                            this.application = data;
                            this.disableForms();
                        });
                }
            });
        } else {
            this._snackBar.open('Envie o vídeo e no mínimo uma foto para finalizar a inscrição. Não se esqueça de responder todas as perguntas!', 'OK');
        }
    }

    disableForms() {
        if(this.application?.status !== constants.APPLICATION_STATUS.PENDENTE){
            this.infoFormGroup.disable();
            this.regionFormGroup.disable();
            this.midiaFormGroup.disable();
            this.sectionsFormGroup.disable();
        }
    }

    isEntregue(){
        return this.application?.id && this.application?.status !== constants.APPLICATION_STATUS.PENDENTE
    }

    deleteApplication(){
        this._snackBar.open('Tem certeza que deseja excluir a inscrição?', 'Sim', {
            duration: 10000,
        }).onAction().subscribe(() => {
            this._applicationService.delete(this.application?.id!)
                .pipe(catchError((err: any) => {
                    this._snackBar.open(err.error.detail ?? 'Erro ao excluir inscrição', 'OK');
                    throw err;
                }))
                .subscribe((data: any) => {
                    this._snackBar.open('Inscrição excluída com sucesso.', 'OK');
                    this.logout();
                });
            }
        );
    }

    deleteCandidate(){
        this._snackBar.open('Tem certeza que deseja excluir o cadastro?', 'Sim', {
            duration: 10000,
        }).onAction().subscribe(() => {
            this._candidateService.delete(this.candidate?.id!)
                .pipe(catchError((err: any) => {
                    this._snackBar.open(err.error.detail ?? 'Erro ao excluir cadastro', 'OK');
                    throw err;
                }))
                .subscribe((data: any) => {
                    this._snackBar.open('Cadastro excluído com sucesso.', 'OK');
                    this.logout();
                });
            }
        );
    }
}
