# ### ===============================================================
# ### ===============================================================
# ### Modify the dataset loading settings

# dataset settings
dataset_type = 'ExampleDataset'
data_root = '/home/alec/Desktop/ImgClassification/data/'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
train_pipeline = [
    dict(type='LoadImagePairFromFile'),
    dict(type='RandomResizedCrop', size=224),
    dict(type='RandomFlip', flip_prob=0.5, direction='horizontal'),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='ImageToTensor', keys=['img1', 'img2']),
    dict(type='ToTensor', keys=['gt_label']),
    dict(type='Collect', keys=['img1', 'img2', 'gt_label']),
]
test_pipeline = [
    dict(type='LoadImagePairFromFile'),
    dict(type='Resize', size=(256, -1)),
    dict(type='CenterCrop', crop_size=224),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='ImageToTensor', keys=['img1', 'img2']),
    dict(type='Collect', keys=['img1', 'img2']),
]

data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type='RepeatDataset',
        times=1,
        dataset=dict(
            type=dataset_type,
            ann_file='train.txt',
            data_prefix= data_root + 'Latin/',
            pipeline=train_pipeline),
        pipeline=train_pipeline
    ),
    val=dict(
        type=dataset_type,
        ann_file='test.txt',
        data_prefix= data_root + 'Latin/',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        ann_file='test.txt',
        data_prefix= data_root + 'Latin/',
        pipeline=test_pipeline))

evaluation = dict(interval=1, metric='mse')

# Set up working dir to save files and logs.
work_dir = '/home/alec/Desktop/ImgClassification/working_dir'


### ===============================================================
### ===============================================================
### Modify the model settings

# model settings
model = dict(
    type='SiameseClassifier',
    pretrained='torchvision://resnet18',
    backbone=dict(
        type='ResNet',
        depth=18,
        num_stages=4,
        out_indices=(3,),
        style='pytorch'),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(
        type='SiameseLinearHead',
        num_classes=1,
        in_channels=512,
        distance='abs',
        loss=dict(type='CrossEntropyLoss', use_sigmoid=True),
    ))


### ===============================================================
### ===============================================================
### Modify the schedule settings

# The original learning rate (LR) is set for 8-GPU training.
# We divide it by 4 since we only use one GPU.
# optimizer
optimizer_lr = 0.001 #0.01 / 4

# optimizer
optimizer = dict(type='SGD', lr=optimizer_lr, momentum=0.9, weight_decay=0.0001, paramwise_cfg=dict(bias_lr_mult=2., bias_decay_mult=0.))
optimizer_config = dict(grad_clip=None)
# learning policy
lr_config = dict(
    policy='step',
    # warmup='linear',
    # warmup_iters=500,
    # warmup_ratio=0.001,
    step=[8, 11])
runner = dict(type='EpochBasedRunner', max_epochs=12)


### ===============================================================
### ===============================================================
### Modify the default runtime settings

checkpoint_config = dict(interval=1)
# yapf:disable
log_config = dict(
    interval=1, #50,
    hooks=[
        dict(type='TextLoggerHook'),
        # dict(type='TensorboardLoggerHook')
    ])

dist_params = dict(backend='nccl')
log_level = 'INFO'
#load_from = None
resume_from = None
#workflow = [('train', 1)]


#log_config.interval = 1

# load model
load_from = None

# run train iter 1 time (overall 1 time which includes: div num_images by batch_size, and mult by dataset_repeat_times)
# run validation iter 1 time 
# only setting workflow = [('train', 1)] will not backpropagate validation error/loss through the network  
workflow = [('train', 1), ('val', 1)]


### ===============================================================
### ===============================================================
### Miscellaneous settings

# Set seed thus the results are more reproducible
seed = 0
#set_random_seed(0, deterministic=False)
gpu_ids = range(1)


### ===============================================================
### ===============================================================
### testing/prediction/evaluation phase - Model settings 

# get the root path to the model checkpoints
ckp_root = work_dir #'/home/tsm/Code/mmdetection/demo/tutorial_exps/'

# models to use for prediction (temporal)
ckp_list = [
                'epoch_11.pth', 
                'epoch_4.pth', 
                'epoch_7.pth', 
                'epoch_6.pth',
                'epoch_12.pth'
            ]
